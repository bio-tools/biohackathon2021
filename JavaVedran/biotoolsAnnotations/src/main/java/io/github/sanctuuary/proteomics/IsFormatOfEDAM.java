package io.github.sanctuuary.proteomics;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.json.JSONException;
import org.json.JSONObject;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;

import nl.uu.cs.ape.sat.APE;
import nl.uu.cs.ape.sat.configuration.APEConfigException;
import nl.uu.cs.ape.sat.configuration.APECoreConfig;
import nl.uu.cs.ape.sat.core.solutionStructure.SolutionsList;
import nl.uu.cs.ape.sat.models.AllModules;
import nl.uu.cs.ape.sat.models.AllTypes;
import nl.uu.cs.ape.sat.models.AuxTypePredicate;
import nl.uu.cs.ape.sat.models.Module;
import nl.uu.cs.ape.sat.models.Pair;
import nl.uu.cs.ape.sat.models.logic.constructs.TaxonomyPredicate;
import nl.uu.cs.ape.sat.utils.APEDimensionsException;
import nl.uu.cs.ape.sat.utils.APEDomainSetup;
import nl.uu.cs.ape.sat.utils.APEUtils;
import nl.uu.cs.ape.sat.utils.OWLReader;

public class IsFormatOfEDAM {
	
	
	public static void getEDAMData() throws APEDimensionsException, OWLOntologyCreationException, JSONException, IOException {
		
		String toolAnnotations = Utils.TOOLS_DIR + Utils.PRE_BIOHACKATHON + "toolAnnotationMetabolomics.json";
		File baseConfiguration = new File(Utils.CONFIGURATION_DIR + "baseape.configuration");
		JSONObject coreConfigJson = APEUtils.readFileToJSONObject(baseConfiguration);
		coreConfigJson = updateCoreConfig(coreConfigJson, "tool_annotations_path", toolAnnotations);
		coreConfigJson = updateCoreConfig(coreConfigJson, "strict_tool_annotations", "false");
		
		
		APECoreConfig config = new APECoreConfig(coreConfigJson);
		APEDomainSetup apeDomainSetup = new APEDomainSetup(config);

		OWLReader owlReader = new OWLReader(apeDomainSetup, config.getOntologyFile());
		boolean ontologyRead = owlReader.readOntology();

		if (!ontologyRead) {
			System.out.println("Error occurred while reading the provided ontology.");
			return;
		}
		
		apeDomainSetup.updateToolAnnotationsFromJson(APEUtils.readFileToJSONObject(config.getToolAnnotationsFile()));
		
		System.out.println("___________________________________");
		
		
		ExtendedOWLReader extOwlReader = new ExtendedOWLReader(apeDomainSetup, config.getOntologyFile());
		
		Map<String, Set<String>> dataTypeFormatDependencies = extOwlReader.getObjectProperties(Utils.DATA_FORMAT_IRI, "http://edamontology.org/is_format_of");
		
		AllTypes allTypes = apeDomainSetup.getAllTypes();
		printStringMap(dataTypeFormatDependencies, allTypes);
		
		
//		Map<String, Set<String>> operationDataTypeInDependencies = extOwlReader.getObjectProperties(Utils.DATA_FORMAT_IRI, "http://edamontology.org/has_input");
//		Map<String, Set<String>> operationDataTypeOutDependencies = extOwlReader.getObjectProperties(Utils.DATA_FORMAT_IRI, "http://edamontology.org/has_output");
		
		
	}
	

	private static void printStringMap(Map<String, Set<String>> dataTypeFormatDependencies, AllTypes allTypes) {
		
		
		for(String formatID : dataTypeFormatDependencies.keySet()) {
			System.out.println(allTypes.get(formatID, Utils.DATA_FORMAT_IRI) + " ->");
			dataTypeFormatDependencies.get(formatID).forEach(dataID -> System.out.println(allTypes.get(dataID, Utils.DATA_TYPE_IRI) + " "));
			System.out.println("_____________________");
		}
		
		System.out.println("Number of formats annotated: " + dataTypeFormatDependencies.keySet().size());
		
	}


	private static String createCSVRow(String predicateLabel, String orderNo, String dataDepth, String formatDepth) {
		String csvROw = predicateLabel.replace(",", ";") + "\t " + orderNo + "\t " + dataDepth + "\t" + formatDepth + "\n"; 
		return csvROw;
	}

	/**
	 * Calculate the furtherest leaf in the taxonomy from the currData class.
	 * @param currData - class in the taxonomy that is evaluated
	 * @return
	 */
	private static int calculateDepth(TaxonomyPredicate currData) {
		int maxDepth = 0;
		for(TaxonomyPredicate subData : APEUtils.safe(currData.getSubPredicates())) {
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
			APEUtils.write2file(createCSVRow("Name", "OrderNo", "Data Depth", "Format depth"), getOutFile(resultFilePath), true);
		} catch (Exception e) {
			// skip
			System.err.println("Delete failed.");
		}
		try {
			APEUtils.write2file(createCSVRow("Name", "OrderNo", "Data Depth", "Format depth"), getInFile(resultFilePath), true);
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
