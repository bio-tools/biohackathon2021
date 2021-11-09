package io.github.sanctuuary.proteomics;

import java.io.IOException;


public class App 
{

	public static void main(String[] args) throws IOException {
		
		IsFormatOfEDAM.defineRelations(Utils.EDAM_ONTOLOGY_FILE);
//		ConfiguringDomain.setupDomain();
		AnnotationQualityEvaluation.evaluateAllAnnotations(Utils.TOOLS_DIR + Utils.PRE_BIOHACKATHON, Utils.RESULTS_DIR + Utils.PRE_BIOHACKATHON);

		System.out.println("end");
	
		}
}
