package io.github.sanctuuary.proteomics;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.SortedSet;
import java.util.stream.Collectors;

import org.json.JSONException;
import org.json.JSONObject;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;

import nl.uu.cs.ape.sat.APE;
import nl.uu.cs.ape.sat.configuration.APEConfigException;
import nl.uu.cs.ape.sat.core.solutionStructure.SolutionsList;
import nl.uu.cs.ape.sat.models.AllTypes;
import nl.uu.cs.ape.sat.models.AuxTypePredicate;
import nl.uu.cs.ape.sat.models.Module;
import nl.uu.cs.ape.sat.models.Pair;
import nl.uu.cs.ape.sat.models.Type;
import nl.uu.cs.ape.sat.models.logic.constructs.TaxonomyPredicate;
import nl.uu.cs.ape.sat.utils.APEDimensionsException;
import nl.uu.cs.ape.sat.utils.APEUtils;

public class AnnotationQualityImplementation {

	private String toolAnnotations;
	private String resultsDir;
	private APE apeFramework;
	private Map<String, Set<String>> dataTypeFormatDependencies;
	private List<BioToolsImprovement> bioToolImprovements;

	public AnnotationQualityImplementation(String toolAnnotationDirPath, String resultsDirPath) {
		List<String> toolAnnotationsDomain = Arrays.asList("toolAnnotationFullBioTools", "toolAnnotationMetabolomics",
				"toolAnnotationProteomics", "toolAnnotationOriginal");

		for (String toolsName : Utils.getElements(toolAnnotationsDomain, 1)) {
			toolAnnotations = toolAnnotationDirPath + toolsName + ".json";
			resultsDir = resultsDirPath + toolsName;
		}
		bioToolImprovements = new ArrayList<BioToolsImprovement>();
	}

	/**
	 * Function used to setup APE framework in bioinformatics using the bio.tools
	 * annotation.
	 * 
	 * @throws IOException
	 */
	public void setupAPE() throws IOException {

		File baseConfiguration = new File(Utils.CONFIGURATION_DIR + "baseape.configuration");

		JSONObject coreConfigJson = APEUtils.readFileToJSONObject(baseConfiguration);
		coreConfigJson = updateCoreConfig(coreConfigJson, "tool_annotations_path", toolAnnotations);
		coreConfigJson = updateCoreConfig(coreConfigJson, "strict_tool_annotations", "false");

		apeFramework = null;
		try {
			// set up the APE framework
			apeFramework = new APE(coreConfigJson);

		} catch (APEConfigException e) {
			System.err.println("Error in setting up the APE framework. APE configuration error:");
			System.err.println(e.getMessage());
			return;
		} catch (JSONException e) {
			System.err.println(
					"Error in setting up the APE framework. Bad JSON formatting (APE configuration or tool annotation JSON). ");
			System.err.println(e.getMessage());
			return;
		} catch (IOException e) {
			System.err.println("Error in setting up the APE framework.");
			System.err.println(e.getMessage());
			return;
		} catch (OWLOntologyCreationException e) {
			System.err.println("Error in setting up the APE framework. Bad ontology format.");
			System.err.println(e.getMessage());
			return;
		}
	}

	/**
	 * Retrieve EDAM data properties used to specify dependencies format-type and
	 * operation - input/output.
	 * 
	 * @throws APEDimensionsException
	 * @throws OWLOntologyCreationException
	 * @throws JSONException
	 * @throws IOException
	 */
	public void getEDAMData() throws APEDimensionsException, OWLOntologyCreationException, JSONException, IOException {

		ExtendedOWLReader extOwlReader = new ExtendedOWLReader(apeFramework.getDomainSetup(),
				apeFramework.getConfig().getOntologyFile());

		dataTypeFormatDependencies = extOwlReader.getObjectProperties(Utils.DATA_FORMAT_IRI,
				"http://edamontology.org/is_format_of");

		AllTypes allTypes = apeFramework.getDomainSetup().getAllTypes();
		Utils.printStringMap(dataTypeFormatDependencies, allTypes, allTypes);

//		Map<String, Set<String>> operationDataTypeInDependencies = extOwlReader.getObjectProperties(Utils.DATA_FORMAT_IRI, "http://edamontology.org/has_input");
//		Map<String, Set<String>> operationDataTypeOutDependencies = extOwlReader.getObjectProperties(Utils.DATA_FORMAT_IRI, "http://edamontology.org/has_output");

	}

	/**
	 * Evaluate the quality of fetched bio.tools based on the EDAM annotations.
	 */
	public void evalateBioTools() {
		for (TaxonomyPredicate abstractModule : apeFramework.getDomainSetup().getAllModules().getModules()) {
			if (abstractModule instanceof Module) {
				Module module = (Module) abstractModule;
				for (Type input : module.getModuleInput()) {
					
					evaluateInputOutput(module, input, "input");
				}
				
				for (Type output : module.getModuleOutput()) {
					
					evaluateInputOutput(module, output, "output");
				}

			}
		}
		BioToolsImprovement.setupHeader(resultsDir + "_suggestions.csv");
		
		bioToolImprovements.forEach(impr -> impr.print2CSV(resultsDir + "_suggestions.csv"));

	}

	private void evaluateInputOutput(Module module, Type input, String infoIO) {

		
		SortedSet<TaxonomyPredicate> predicates = ((AuxTypePredicate) input).getGeneralizedPredicates();
//		predicates.first().getRootNodeID()
		TaxonomyPredicate dataFormat = predicates.stream()
				.filter(x -> x.getRootNodeID().equals(Utils.DATA_FORMAT_IRI)).findFirst().get();
		if (dataFormat instanceof AuxTypePredicate) {
			return;
		}
		/* Check if the format was annotated using the EDAM format/type dependencies. */
		if (dataTypeFormatDependencies.get(dataFormat.getPredicateID()) == null) {
			return;
		}

		TaxonomyPredicate dataType = predicates.stream()
				.filter(x -> x.getRootNodeID().equals(Utils.DATA_TYPE_IRI)).findFirst().get();

		if (dataType instanceof AuxTypePredicate) {
			return;
		}

		Set<String> altTypeIDs = evaluateFormatTypeDepencency(module, dataFormat, dataType);
		
		if(altTypeIDs.size() > 0) {
			AllTypes allTypes = apeFramework.getDomainSetup().getAllTypes();
			Set<TaxonomyPredicate> altTypes = altTypeIDs.stream().map(typeID -> allTypes.get(typeID))
														.collect(Collectors.toSet());
			bioToolImprovements.add(new BioToolsImprovement(module, infoIO , dataFormat, dataType, altTypes));
			
		}
	
		
	}

	/**
	 * Evaluate the relation between the given and expected data type.
	 * @param usedDataFormat
	 * @param usedDataType
	 * @param dataType 
	 * @return
	 */
	private Set<String> evaluateFormatTypeDepencency(TaxonomyPredicate module, TaxonomyPredicate usedDataFormat, TaxonomyPredicate usedDataType) {
		
		Set<String> setOfNewTypes = new HashSet<String>();
		
		Set<String> expectedDataTypeIDs = dataTypeFormatDependencies.get(usedDataFormat.getPredicateID());
		
		for (String expectedDataTypeID : expectedDataTypeIDs) {
			TaxonomyPredicate expectedDataType = apeFramework.getDomainSetup().getAllTypes().get(expectedDataTypeID);
			
			if(isTermMoreSpecific(module, expectedDataType, usedDataType, true)) {
				setOfNewTypes.add(expectedDataTypeID);
			}
		}
		
		return setOfNewTypes;
	}
	

	private boolean isTermMoreSpecific(TaxonomyPredicate module, TaxonomyPredicate expectedDataType, TaxonomyPredicate usedDataType, boolean firstCall) {
		boolean moreSpecific = false;

		if(firstCall && usedDataType.equals(expectedDataType)) {
			System.out.println("This tool " + module.getPredicateLabel() + " is verified and aligns with EDAM.");
			return false;
		}
		
		// test if it is superclass? bio.tools are better in that case
		for(TaxonomyPredicate subType : usedDataType.getSubPredicates()) {
			if(subType.equals(expectedDataType)) {
				return true;
			} else {
				moreSpecific = moreSpecific || isTermMoreSpecific(module, expectedDataType, subType, false);
			}
		}
		
		return moreSpecific;
	}

	private static String createCSVRow(String predicateLabel, String orderNo, String dataDepth, String formatDepth) {
		String csvROw = predicateLabel.replace(",", ";") + "\t " + orderNo + "\t " + dataDepth + "\t" + formatDepth
				+ "\n";
		return csvROw;
	}

	/**
	 * Calculate the furtherest leaf in the taxonomy from the currData class.
	 * 
	 * @param currData - class in the taxonomy that is evaluated
	 * @return
	 */
	private static int calculateDepth(TaxonomyPredicate currData) {
		int maxDepth = 0;
		for (TaxonomyPredicate subData : APEUtils.safe(currData.getSubPredicates())) {
			int newDepth = calculateDepth(subData) + 1;
			maxDepth = Math.max(maxDepth, newDepth);
		}

		return maxDepth;
	}

	private static File getOutFile(String resultFilePath) {
		return new File(resultFilePath + "_outputs.csv");
	}

	private static File getInFile(String resultFilePath) {
		return new File(resultFilePath + "_inputs.csv");
	}

	private static void deleteExistingResults(String resultFilePath) {
		try {
			getOutFile(resultFilePath).delete();
		} catch (Exception e) {
			// skip
			System.err.println("Delete failed.");
		}
		try {
			getInFile(resultFilePath).delete();
		} catch (Exception e) {
			// skip
			System.err.println("Delete failed.");
		}

	}

	private static void setupHeaders(String resultFilePath) {
		try {
			APEUtils.write2file(createCSVRow("Name", "OrderNo", "Data Depth", "Format depth"),
					getOutFile(resultFilePath), true);
		} catch (Exception e) {
			// skip
			System.err.println("Delete failed.");
		}
		try {
			APEUtils.write2file(createCSVRow("Name", "OrderNo", "Data Depth", "Format depth"),
					getInFile(resultFilePath), true);
		} catch (Exception e) {
			// skip
			System.err.println("Delete failed.");
		}

	}

	public static String concat(String... strings) {
		String concat = "";
		for (String s : strings) {
			if (s != "") {
				concat += s + "_";
			}
		}
		return APEUtils.removeLastChar(concat);
	}

	/**
	 * Update tool annotation field in the configuration file.
	 * 
	 * @param coreConfigJson
	 * @param toolAnnotationsPath
	 * @return
	 * @throws JSONException
	 * @throws IOException
	 */
	private static JSONObject updateCoreConfig(JSONObject coreConfigJson, String tag, String toolAnnotationsPath)
			throws JSONException, IOException {
		coreConfigJson.put(tag, toolAnnotationsPath);
		return coreConfigJson;
	}

	private static boolean writeCSVSolutionStatistics(SolutionsList solutions, File output) throws IOException {
		StringBuilder solutionsFoundCSV = new StringBuilder("Length, Solutions\n");
		for (Pair<Integer> solutionsForLength : solutions.getSolutionsPerLength()) {
			solutionsFoundCSV = solutionsFoundCSV.append(solutionsForLength.getFirst()).append(",")
					.append(solutionsForLength.getSecond()).append("\n");
		}
		APEUtils.write2file(solutionsFoundCSV.toString(), output, false);
		return true;
	}

}
