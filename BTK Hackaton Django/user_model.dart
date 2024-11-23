import 'package:yks/models/daily_report_model_ayt.dart';
import 'package:yks/models/daily_report_model_tyt.dart';

class UserModel {
  final String uid;
  final String name;
  final String surName;
  final DateTime birthDate;
  final String field;
  final List<DailyReportModelTYT> dailyReportListTYT;
  final List<DailyReportModelAYT> dailyReportListAYT;

  UserModel(
    this.uid,
    this.name,
    this.surName,
    this.field,
    this.dailyReportListTYT,
    this.dailyReportListAYT,
    this.birthDate,
  );
}
