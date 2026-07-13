import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';

class SearchPage extends StatefulWidget {
  const SearchPage({super.key});

  @override
  _SearchPageState createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  @override
  Widget build(BuildContext context) {
    return PlatformScaffold(
      iosContentPadding: true,
      appBar: PlatformAppBar(
        title: PlatformTextField(
          material: (_, __) => MaterialTextFieldData(
            decoration: const InputDecoration(
              hintText: 'Search...',
              border: OutlineInputBorder(),
            ),
          ),
          cupertino: (_, __) => CupertinoTextFieldData(
            placeholder: 'Search...',
          ),
        ),
      ),
      body: Column(
        children: [
          // FIXED: Wrap the Row in Padding, not the Expanded widgets
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                // Use Expanded directly in Row, not wrapped in Padding
                Expanded(
                  child: Padding( // Add padding INSIDE the Expanded if needed
                    padding: const EdgeInsets.symmetric(horizontal: 4.0),
                    child: PlatformElevatedButton(
                      onPressed: () {},
                      child: const Text('Memers'),
                    ),
                  ),
                ),
                Expanded(
                  child: Padding( // Add padding INSIDE the Expanded if needed
                    padding: const EdgeInsets.symmetric(horizontal: 4.0),
                    child: PlatformElevatedButton(
                      onPressed: () {},
                      child: const Text('Posts'),
                    ),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: GridView.builder(
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 3,
                crossAxisSpacing: 1,
                mainAxisSpacing: 1,
              ),
              itemBuilder: (context, index) {
                return ColoredBox(
                  color: Colors.blue,
                  child: Center(
                    child: Text('Item $index'),
                  ),
                );
              },
              itemCount: 20,
            ),
          ),
        ],
      ),
    );
  }
}
