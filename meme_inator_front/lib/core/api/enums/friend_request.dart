/// Friend request type enum
enum FriendRequestType {
  incoming('incoming'),
  outgoing('outgoing');

  final String value;
  const FriendRequestType(this.value);
  
  @override
  String toString() => value;
}