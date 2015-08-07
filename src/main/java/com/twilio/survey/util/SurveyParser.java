package com.twilio.survey.util;

import com.twilio.survey.models.Question;
import com.twilio.survey.models.Survey;
import com.twilio.survey.services.QuestionService;
import com.twilio.survey.services.SurveyService;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.springframework.transaction.annotation.Transactional;


import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Date;

public class SurveyParser {
  SurveyService surveyService;
  QuestionService questionService;

  public SurveyParser() {}

  public SurveyParser(SurveyService surveyService, QuestionService questionService) {
    this.surveyService = surveyService;
    this.questionService = questionService;
  }

  public void parse(String fileName) {
    FileReader reader = null;
    try {
      reader = new FileReader(fileName);
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }
    JSONParser jsonParser = new JSONParser();
    JSONObject jsonObject = null;
    try {
      jsonObject = (JSONObject) jsonParser.parse(reader);
    } catch (IOException e) {
      System.out.println("Error reading from survey file");
    } catch (ParseException e) {
      System.out.println("Error while parsing JSON survey file");
    }

    String title = (String) jsonObject.get("title");
    JSONArray questions = (JSONArray) jsonObject.get("questions");

    insertSurveyIntoDb(title,questions);
  }

  @Transactional
  private void insertSurveyIntoDb(String title, JSONArray questions) {
    Survey survey = new Survey(title, new Date());
    surveyService.create(survey);
    Question newQuestion;

    for(Object question : questions) {
      JSONObject obj = (JSONObject) question;
      String body = (String) obj.get("body");
      String type = (String) obj.get("type");
      newQuestion = new Question(body, type, survey, new Date());
      questionService.create(newQuestion);
    }
  }
}