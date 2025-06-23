class UserInfo {
  final String id;
  final String name;
  final String email;

  UserInfo({
    required this.id, 
    required this.name, 
    required this.email,
  });

  factory UserInfo.fromJson(Map<String, dynamic> json) {
    return UserInfo(
      id: json['id'] ?? 'empty!', 
      name: json['name'] ?? 'empty!', 
      email: json['email'] ?? 'empty!',
    );
  }

  Map<String, dynamic> toJson() {
    return {'id': id, 'name': name, 'email': email};
  }
}
