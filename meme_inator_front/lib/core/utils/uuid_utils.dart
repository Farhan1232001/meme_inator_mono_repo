import 'package:uuid/uuid_value.dart';

UuidValue uuidFromJson(String uuid) => UuidValue.fromString(uuid);
String uuidToJson(UuidValue uuid) => uuid.toString();
