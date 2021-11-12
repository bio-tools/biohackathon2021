package io.github.sanctuuary.proteomics.dataRetrieval;

import java.io.File;
import java.io.IOException;

import org.json.JSONArray;
import org.json.JSONObject;

import io.github.sanctuuary.proteomics.Utils;
import nl.uu.cs.ape.sat.utils.APEUtils;

public class ConfiguringDomain {

	
	public static void setupDomain() throws IOException {
//		getLimitedToolSet(Utils.TOOLS_DIR + "toolList.json");
//		System.out.println();
//		getToolSetFromDomain("proteomics", "Proteomics");
		
		System.out.println();
		getToolSetFromEDAMTopic("topic_3538", "Protein disordered structure");
//		
//		System.out.println();
//		getToolSetFromDomain("", "FullBioTools");
	}
	
	/**
	 * Fetching and processing a limited set of bio.tools enumerated in a file.
	 * @param listFilePath
	 * @throws IOException
	 */
	private static void getLimitedToolSet(String listFilePath) throws IOException {
		String toolType = "Original";
		
		// Fetch the Limited (predefined) set of tool
		JSONArray bioToolsRAW = BioToolsAPI.readListOfTools(listFilePath);
		
		APEUtils.write2file(bioToolsRAW.toString(), new File(Utils.TOOLS_DIR + Utils.TOOLS_PREFIX + toolType + "RAW.json"), false);
		
		JSONObject apeToolAnnotation = BioToolsAPI.convertBioTools2ApeAnnotation(bioToolsRAW);
		APEUtils.write2file(apeToolAnnotation.toString(), new File(Utils.TOOLS_DIR + Utils.PRE_BIOHACKATHON + Utils.TOOLS_PREFIX + toolType + ".json"), false);
	}
	
	
	
	/**
	 * Fetching and processing bio.tools that belong to a specific domain.
	 * @throws IOException
	 */
	private static void getToolSetFromDomain(String domainName, String toolType) throws IOException {

		// Fetch the Extended set of tool
		JSONArray bioToolsRAW = BioToolsAPI.getToolsFromDomain(domainName);
		
		APEUtils.write2file(bioToolsRAW.toString(), new File(Utils.TOOLS_DIR + Utils.TOOLS_PREFIX + toolType + "RAW.json"), false);
		
		JSONObject apeToolAnnotation = BioToolsAPI.convertBioTools2ApeAnnotation(bioToolsRAW);
		APEUtils.write2file(apeToolAnnotation.toString(), new File(Utils.TOOLS_DIR + Utils.TOOLS_PREFIX + toolType + ".json"), false);
	}
	
	
	/**
	 * Fetching and processing bio.tools that belong to a certain EDAM topic.
	 * @throws IOException
	 */
	private static void getToolSetFromEDAMTopic(String topicName, String toolType) throws IOException {

		// Fetch the Extended set of tool
		JSONArray bioToolsRAW = BioToolsAPI.getToolsFromEDAMTopic(topicName);
		
		APEUtils.write2file(bioToolsRAW.toString(), new File(Utils.TOOLS_DIR + Utils.TOOLS_PREFIX + toolType + "RAW.json"), false);
		
		JSONObject apeToolAnnotation = BioToolsAPI.convertBioTools2ApeAnnotation(bioToolsRAW);
		APEUtils.write2file(apeToolAnnotation.toString(), new File(Utils.TOOLS_DIR + Utils.TOOLS_PREFIX + toolType + ".json"), false);
	}
	
	/**
	 * Processing bio.tools that were already fetched from bio.tool
	 * @throws IOException
	 */
	private static void setupToolSetFromExistingDomain(String notNeededField, String toolType) throws IOException {

		JSONArray bioToolsRAW = APEUtils.readFileToJSONArray(new File(Utils.TOOLS_DIR + Utils.TOOLS_PREFIX + toolType + "RAW.json"));
		
		
		JSONObject apeToolAnnotation = BioToolsAPI.convertBioTools2ApeAnnotation(bioToolsRAW);
		APEUtils.write2file(apeToolAnnotation.toString(), new File(Utils.TOOLS_DIR + Utils.TOOLS_PREFIX + toolType + ".json"), false);
	}
	
}
