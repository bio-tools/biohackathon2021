package io.github.sanctuuary.proteomics;

import nl.uu.cs.ape.sat.models.AbstractModule;
import nl.uu.cs.ape.sat.models.AllModules;
import nl.uu.cs.ape.sat.models.AllTypes;
import nl.uu.cs.ape.sat.models.Type;
import nl.uu.cs.ape.sat.models.enums.NodeType;
import nl.uu.cs.ape.sat.utils.APEDimensionsException;
import nl.uu.cs.ape.sat.utils.APEDomainSetup;

import org.apache.commons.io.FileExistsException;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.reasoner.structural.StructuralReasonerFactory;
import org.semanticweb.owlapi.search.EntitySearcher;

import java.io.File;
import java.util.*;
import java.util.logging.Logger;
import java.util.stream.Collectors;

/**
 * The {@code ExtendedOWLReader} class is used to extract the classification information
 * regarding the modules and data types from the OWL ontology.
 *
 * @author Vedran Kasalica
 */
public class ExtendedOWLReader {

	/** File cinstianing the ontology */
	private final File ontologyFile;
	/** List of all modules in the domain */
	private final AllModules allModules;
	/** List of all types in the domain */
	private final AllTypes allTypes;
	/** Mapping from each dimension to the list of the types within it */
	private Map<String, Set<String>> typeDimensions = new HashMap<String, Set<String>>();
	
	private OWLOntology ontology;
	private OWLDataFactory factory;
	/** OWL logger */
	private Logger logger = Logger.getLogger("ExtendedOWLReader.class");
	/** Holds information whether the domain was annotated under the strict rules of the output dependency. */
	private boolean useStrictToolAnnotations;

	/**
	 * Setting up the reader that will populate the provided module and type sets
	 * with objects from the ontology.
	 *
	 * @param domain       Domain information, including all the existing tools and types.
	 * @param ontologyFile Path to the OWL file.
	 */
	public ExtendedOWLReader(APEDomainSetup domain, File ontologyFile) {
		this.ontologyFile = ontologyFile;
		this.allModules = domain.getAllModules();
		this.allTypes = domain.getAllTypes();
		this.factory = OWLManager.getOWLDataFactory();
		this.useStrictToolAnnotations = domain.getUseStrictToolAnnotations();
	}

	public Map<String, Set<String>> getFormatTypeDependencies(String dataFormatIRI) throws OWLOntologyCreationException {
		/** Mapping from a data type/format to all relevant format/data types. */
		Map<String, Set<String>> dataFormatDependencies = new HashMap<String, Set<String>>();

		final OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		if (this.ontologyFile.exists()) {
			this.ontology = manager.loadOntologyFromOntologyDocument(ontologyFile);
		} else {
			this.logger.warning("Provided ontology does not exist.");
			return null;
		}
		OWLReasonerFactory reasonerFactory = new StructuralReasonerFactory();
		OWLReasoner reasoner = reasonerFactory.createNonBufferingReasoner(ontology);

		/* Get a root of the data format taxonomy. */
		OWLClass formatRootClass = manager.getOWLDataFactory().getOWLClass(IRI.create(dataFormatIRI));
		if (!ontology.containsClassInSignature(IRI.create(dataFormatIRI))) {
			/* Handle scenario when the tool taxonomy root was not defined properly. */
			throw APEDimensionsException.notExistingDimension(String.format("Operation root %s does not exist in the ontology.", dataFormatIRI));
		}

		
		exploreTypeFormatDepencencyRec(dataFormatDependencies, reasoner, formatRootClass, new HashSet<String>());

		return dataFormatDependencies;
	}
	

	/**
	 * Recursively exploring the hierarchy of the data format ontology and defining 
	 * relations between data type and data format objects ({@link Type}).
	 *
	 * @param dataFormatDependencies - Existing data/format dependencies
	 * @param reasoner   Reasoner used to provide subclasses.
	 * @param currClass  The class (node) currently explored.
	 * @param superClass The superclass of the currClass.
	 */
	private void exploreTypeFormatDepencencyRec(Map<String, Set<String>> dataFormatDependencies, OWLReasoner reasoner, OWLClass currClass, Set<String> dependantDataTypes) {

		final OWLClass currRoot;
		Type superType = null;
		Type currType = null;
			
		superType = allTypes.get(getIRI(superClass), getIRI(rootClass));
		/*
		 * Check whether the current node is a root or subRoot node.
		 */
		NodeType currNodeType = NodeType.ABSTRACT;
		if (allTypes.getDataTaxonomyDimensionIDs().contains(getIRI(currClass))) {
			currNodeType = NodeType.ROOT;
			currRoot = currClass;
		} else {
			currRoot = rootClass;
		}

		currType = addNewTypeToAllTypes(getLabel(currClass), getIRI(currClass), getIRI(currRoot), currNodeType);

		
		/* Add the current type as a sub-type of the super type. */
		if (superType != null && currType != null) {
			superType.addSubPredicate(currType);
		}
		/* Add the super-type for the current type */
		if (currNodeType != NodeType.ROOT) {
			currType.addSuperPredicate(superType);
		}

		List<OWLClass> subClasses = reasoner.getSubClasses(currClass, true).entities()
				.filter(child -> reasoner.isSatisfiable(child)).collect(Collectors.toList());

		subClasses.forEach(child -> exploreTypeOntologyRec(reasoner, child, currClass, currRoot));

		if (subClasses.isEmpty()) {
			currType.setNodePredicate(NodeType.LEAF);
		} else if (useStrictToolAnnotations) {
			Type artificialSubType = addNewTypeToAllTypes(getLabel(currClass) + "_p", getIRI(currClass) + "_plain",
					getIRI(currRoot), NodeType.ARTIFICIAL_LEAF);
			if (artificialSubType != null) {
				currType.addSubPredicate(artificialSubType);
				currType.setPlainType(artificialSubType);
				
				artificialSubType.addSuperPredicate(currType);
				artificialSubType.setNodePredicate(NodeType.LEAF);
			} else {
				System.err.println("Artificial predicate '" + getLabel(currClass) + "' was not created correctly.");
			}
		}
	}
	
	private Type addNewTypeToAllTypes(String classLabel, String classID, String rootID, NodeType currNodeType) {
		Type currType = null;
		/* Generate the Type that corresponds to the taxonomy class. */
		try {
			currType = allTypes
					.addPredicate(new Type(classLabel, classID, rootID, currNodeType));
			typeDimensions.get(rootID).add(classID);
		} catch (ExceptionInInitializerError e) {
			e.printStackTrace();
		}
		return currType;
	}

	/**
	 * Returning the label of the provided OWL class.
	 *
	 * @param currClass Provided OWL class.
	 * @return String representation of the class name.
	 */
	private String getLabel(OWLClass currClass) {
		if (currClass == null || currClass.isOWLNothing()) {
			return "N/A";
		}
		String label, classID = currClass.toStringID();
		Optional<OWLAnnotation> classLabel = EntitySearcher.getAnnotations(currClass, ontology, factory.getRDFSLabel())
				.findFirst();
		if (classLabel.isPresent()) {
			OWLAnnotationValue val = classLabel.get().getValue();
			if (val instanceof OWLLiteral)
				return ((OWLLiteral) val).getLiteral();
		} else if (classID.contains("#")) {
			label = classID.substring(classID.indexOf('#') + 1);
//			label = label.replace(" ", "_");
			return label;
		}
		logger.fine("Class '" + classID + "' has no label.");
		return classID;

	}

	/**
	 * Returning the IRI of the provided OWL class.
	 *
	 * @param currClass Provided OWL class.
	 * @return String representation of the class name.
	 */
	private String getIRI(OWLClass currClass) {
		if (currClass == null) {
			return null;
		}
		return currClass.toStringID();
	}
}
