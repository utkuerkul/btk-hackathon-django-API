class ExamModel {
  final String examType;
  final DateTime date;
  final List<ResultModel> resultList;

  ExamModel(
    this.examType,
    this.date,
    this.resultList,
  );
}

class ResultModel {
  final String field;
  final int trueAnswers;
  final int falseAnswers;
  final double clearAnswers;

  ResultModel(
    this.field,
    this.trueAnswers,
    this.falseAnswers,
    this.clearAnswers,
  );
}

class DailyReportModelTYT {
  final DateTime date;
  final List<ResultModel> dailyList;

  DailyReportModelTYT(
    this.date,
    this.dailyList,
  );
}

class DailyReportModelAYT {
  final DateTime date;
  final List<ResultModel> dailyList;

  DailyReportModelAYT(
    this.date,
    this.dailyList,
  );
}
