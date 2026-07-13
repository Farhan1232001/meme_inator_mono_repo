import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';

/// A dashboard widget displaying the user's profile information including avatar,
/// online status, and stats. Composed within [MenuPage] under User Pages tab.
class ProfileDashboardWidget extends StatefulWidget {
  /// Creates a [ProfileDashboardWidget].
  const ProfileDashboardWidget({super.key});

  @override
  _ProfileDashboardWidgetState createState() => _ProfileDashboardWidgetState();
}

class _ProfileDashboardWidgetState extends State<ProfileDashboardWidget> {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      decoration: BoxDecoration(
        border: Border.all(
          //color: theme.primaryColor,
          width: 2,
        ),
        borderRadius: BorderRadius.circular(10),
        //color: theme.primaryColor,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Column(
            children: [
                Container(
                width: 100,
                height: 100,
                decoration: const BoxDecoration(
                  image: DecorationImage(
                  fit: BoxFit.cover,
                  image: NetworkImage('https://www.cnet.com/a/img/resize/20d6844768bd3f5f0df41deee97897423bcaf3c5/hub/2021/11/03/3c2a7d79-770e-4cfa-9847-66b3901fb5d7/c09.jpg?auto=webp&fit=crop&height=1200&width=1200'),
                  ),
                ),
                ),
              const Row(
                children: [
                  Text('isOnline?: '),
                  Icon(
                    Icons.circle,
                    color: true ? Colors.green : Colors.red,
                    size: 9,
                  ),
                ],
              ),
            ],
          ),
          const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Username: John Doe'),
              Text('Mantra: Just do it'),
              Text('Followers: 1'),
              Text('Followering: 1'),
              Text('B-day: 1/1/1555'),
            ],
          ),
        ],
      ),
    );
  }
}
