package io.github.sanctuuary.proteomics;

import java.io.IOException;

import org.json.JSONException;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;

import nl.uu.cs.ape.sat.utils.APEDimensionsException;


public class App 
{

	public static void main(String[] args) throws IOException, APEDimensionsException, OWLOntologyCreationException, JSONException {
		
//		ConfiguringDomain.setupDomain();
		
		IsFormatOfEDAM.getEDAMData();
		
		AnnotationQualityImprovement.loadData(Utils.TOOLS_DIR, Utils.RESULTS_DIR);
//		AnnotationQualityEvaluation.evaluateAllAnnotations(Utils.TOOLS_DIR, Utils.RESULTS_DIR);
//		AnnotationQualityEvaluation.evaluateAllAnnotations(Utils.TOOLS_DIR + Utils.PRE_BIOHACKATHON, Utils.RESULTS_DIR + Utils.PRE_BIOHACKATHON);

		System.out.println("end");
	
		}
}
