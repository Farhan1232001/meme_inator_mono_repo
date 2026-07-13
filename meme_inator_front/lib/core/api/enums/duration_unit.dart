/// Duration unit enum for sectional feeds
enum DurationUnit {
  day('day'),
  week('week'),
  month('month');

  final String value;
  const DurationUnit(this.value);
  
  @override
  String toString() => value;
}