import 'package:yks/models/daily_work_model.dart';

class DailyReportModelTYT {
  final DateTime date;
  final List<ResultModel> dailyList;

  DailyReportModelTYT(
    this.date,
    this.dailyList,
  );
}
