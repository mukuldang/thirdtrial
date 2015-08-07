package com.twilio.survey;

import com.twilio.survey.models.Survey;
import com.twilio.survey.repositories.QuestionRepository;
import com.twilio.survey.repositories.SurveyRepository;
import com.twilio.survey.services.QuestionService;
import com.twilio.survey.services.SurveyService;
import com.twilio.survey.util.SurveyParser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.Date;

@SpringBootApplication
public class SurveyJavaApplication implements CommandLineRunner {
  @Autowired
  private QuestionRepository questionRepository;
  @Autowired
  private SurveyRepository surveyRepository;

  public static void main(String[] args) {
    SpringApplication.run(SurveyJavaApplication.class, args);
  }

  @Override
  public void run(String... strings) throws Exception {
    SurveyService surveyService = new SurveyService(surveyRepository);
    QuestionService questionService = new QuestionService(questionRepository);

    SurveyParser surveyParser = new SurveyParser(surveyService, questionService);
    surveyParser.parse("survey.json");
  }
}
