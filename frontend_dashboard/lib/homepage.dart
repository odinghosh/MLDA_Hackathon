import 'dart:async';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:pie_chart/pie_chart.dart';

class homePage extends StatefulWidget {
  const homePage({Key? key}) : super(key: key);

  @override
  State<homePage> createState() => _homePageState();
}

class _homePageState extends State<homePage> {
  Timer? timer;
  Map<String, double> dataMap = {"Confused Students": 0, "Alert Students": 0};

  int numberStudent = 0;
  int confusedStudents = 0;
  var db = FirebaseFirestore.instance;
  Future<void> getData() async {
    int tempNumStudent = 0;
    int tempNumConfusedStudent = 0;
    await db.collection('lectures/lecture1/students').get().then((event) {
      for (var doc in event.docs) {
        if (doc.data()['confused']) {
          tempNumConfusedStudent += 1;
        }
        tempNumStudent += 1;
      }
    });
    setState(() {
      dataMap = {
        "Confused Students": tempNumConfusedStudent as double,
        "Alert Students": tempNumStudent - tempNumConfusedStudent as double
      };
    });
  }

  void initState() {
    getData();
    timer = Timer.periodic(Duration(seconds: 3), (timer) async {
      print('running');
      int tempNumStudent = 0;
      int tempNumConfusedStudent = 0;
      await db.collection('lectures/lecture1/students').get().then((event) {
        for (var doc in event.docs) {
          if (doc.data()['confused']) {
            tempNumConfusedStudent += 1;
          }
          tempNumStudent += 1;
        }
      });
      setState(() {
        dataMap = {
          "Confused Students": tempNumConfusedStudent as double,
          "Alert Students": tempNumStudent - tempNumConfusedStudent as double
        };
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return PieChart(
      dataMap: dataMap,
      chartValuesOptions: ChartValuesOptions(showChartValuesInPercentage: true),
    );
  }
}
