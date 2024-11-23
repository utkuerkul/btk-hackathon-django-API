import 'package:yks/models/daily_work_model.dart';

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
