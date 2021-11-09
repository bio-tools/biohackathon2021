package io.github.sanctuuary.proteomics;

import java.util.ArrayList;
import java.util.List;

public class Utils {

	private static String RES_DIR = "./src/main/resources/res/";
	public static String CONFIGURATION_DIR = RES_DIR + "Configurations/";
	public static String CONSTRAINTS_DIR = RES_DIR + "Constraints/";
	public static String RESULTS_DIR = RES_DIR + "Results/";
	public static String TOOLS_DIR = RES_DIR + "ToolAnnotations/";
	public static String EDAM_ONTOLOGY_FILE = RES_DIR + "edam.owl";
	public static String TOOLS_PREFIX = "toolAnnotation";
	public static String PRE_BIOHACKATHON = "November_7/";
	
	
	/**
	 * Get elements of the list given as indexes.
	 * @param list - original list of elements
	 * @param indexes - indexes of the elements that should be retreaved
	 * @return
	 */
	public static List<String> getElements(List<String> list, int... indexes) {
		List<String> elements = new ArrayList<String>();
		for (int index : indexes) {
			elements.add(list.get(index - 1));
		}
		return elements;
	}
}
