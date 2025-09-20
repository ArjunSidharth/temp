import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:convert';
import 'dart:math';

void main() {
  runApp(PondyChatbotApp());
}

class PondyChatbotApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Pondy Travel Companion',
      theme: ThemeData(
        primarySwatch: Colors.orange,
        primaryColor: Color(0xFFE65100),
        accentColor: Color(0xFF2196F3),
        fontFamily: 'Roboto',
      ),
      home: ChatbotHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class ChatbotHomePage extends StatefulWidget {
  @override
  _ChatbotHomePageState createState() => _ChatbotHomePageState();
}

class _ChatbotHomePageState extends State<ChatbotHomePage>
    with TickerProviderStateMixin {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  
  List<ChatMessage> _messages = [];
  String _selectedLanguage = 'English';
  bool _isTyping = false;
  String _userName = '';
  Map<String, dynamic> _userPreferences = {};
  
  // Supported languages
  final Map<String, String> _languages = {
    'English': 'en',
    'French': 'fr',
    'Tamil': 'ta',
    'Hindi': 'hi',
    'Spanish': 'es',
    'German': 'de',
  };
  
  // Sample Pondicherry data (in production, this would come from APIs)
  final Map<String, dynamic> _pondyData = {
    'attractions': {
      'devotional': [
        {
          'name': 'Sri Aurobindo Ashram',
          'description': 'Spiritual center founded by Sri Aurobindo',
          'location': 'White Town',
          'crowd_level': 'moderate',
          'best_time': 'early_morning',
          'story': 'Founded in 1926, this ashram is the heart of Pondicherry\'s spiritual heritage.'
        },
        {
          'name': 'Immaculate Conception Cathedral',
          'description': 'Beautiful French colonial church',
          'location': 'Mission Street',
          'crowd_level': 'low',
          'best_time': 'evening',
          'story': 'Built in 1791, showcasing Gothic architecture with French colonial influence.'
        },
      ],
      'adventure': [
        {
          'name': 'Paradise Beach',
          'description': 'Pristine beach accessible by boat',
          'location': 'Chunnambar',
          'crowd_level': 'high',
          'best_time': 'morning',
          'story': 'A secluded paradise reached through backwater boat rides.'
        },
        {
          'name': 'Scuba Diving at Temple Adventures',
          'description': 'Underwater exploration experience',
          'location': 'Auroville Beach',
          'crowd_level': 'low',
          'best_time': 'afternoon',
          'story': 'Discover the underwater world of the Bay of Bengal.'
        },
      ],
      'party': [
        {
          'name': 'Le Club',
          'description': 'Beachside nightclub with live music',
          'location': 'Promenade Beach',
          'crowd_level': 'high',
          'best_time': 'night',
          'story': 'The hotspot for Pondicherry nightlife since 2010.'
        },
      ]
    },
    'events': [
      {
        'name': 'Bastille Day Celebration',
        'date': '2025-07-14',
        'location': 'French Quarter',
        'description': 'French cultural celebration with parades'
      },
      {
        'name': 'International Yoga Festival',
        'date': '2025-12-21',
        'location': 'Auroville',
        'description': 'Week-long yoga and meditation retreat'
      },
    ],
    'transport': {
      'bike_rentals': [
        {
          'name': 'Pondy Bike Rentals',
          'location': 'Mission Street',
          'price_per_day': 300,
          'types': ['Activa', 'Pulsar', 'Royal Enfield'],
          'contact': '+91-9876543210'
        },
        {
          'name': 'French Quarter Bikes',
          'location': 'Rue Dumas',
          'price_per_day': 250,
          'types': ['Hero Honda', 'Activa'],
          'contact': '+91-9876543211'
        },
      ]
    }
  };

  @override
  void initState() {
    super.initState();
    _initializeChat();
  }

  void _initializeChat() {
    Future.delayed(Duration(milliseconds: 500), () {
      setState(() {
        _messages.add(ChatMessage(
          text: _getLocalizedText('welcome_message'),
          isUser: false,
          timestamp: DateTime.now(),
        ));
      });
    });
  }

  String _getLocalizedText(String key) {
    // Simplified localization - in production, use proper i18n
    Map<String, Map<String, String>> translations = {
      'welcome_message': {
        'en': 'Bonjour! Welcome to Pondicherry! 🌺 I\'m your personal travel companion. What would you like to explore today?',
        'fr': 'Bonjour! Bienvenue à Pondichéry! 🌺 Je suis votre compagnon de voyage personnel. Que souhaitez-vous explorer aujourd\'hui?',
        'ta': 'வணக்கம்! பாண்டிச்சேரிக்கு வரவேற்கிறோம்! 🌺 நான் உங்கள் தனிப்பட்ட பயண துணை. இன்று நீங்கள் என்ன ஆராய விரும்புகிறீர்கள்?',
      },
      'thinking': {
        'en': 'Let me think about that...',
        'fr': 'Laissez-moi réfléchir à cela...',
        'ta': 'அதைப் பற்றி யோசிக்கிறேன்...',
      }
    };
    
    String langCode = _languages[_selectedLanguage] ?? 'en';
    return translations[key]?[langCode] ?? translations[key]?['en'] ?? 'Translation not available';
  }

  void _sendMessage(String text) {
    if (text.trim().isEmpty) return;

    setState(() {
      _messages.add(ChatMessage(
        text: text,
        isUser: true,
        timestamp: DateTime.now(),
      ));
      _isTyping = true;
    });

    _messageController.clear();
    _scrollToBottom();

    // Simulate AI processing
    Future.delayed(Duration(seconds: 2), () {
      String response = _processUserMessage(text);
      setState(() {
        _messages.add(ChatMessage(
          text: response,
          isUser: false,
          timestamp: DateTime.now(),
        ));
        _isTyping = false;
      });
      _scrollToBottom();
    });
  }

  String _processUserMessage(String message) {
    String lowerMessage = message.toLowerCase();
    
    // Intent recognition (simplified)
    if (lowerMessage.contains('temple') || lowerMessage.contains('spiritual') || lowerMessage.contains('devotional')) {
      return _generateDevotionalRecommendations();
    } else if (lowerMessage.contains('adventure') || lowerMessage.contains('beach') || lowerMessage.contains('diving')) {
      return _generateAdventureRecommendations();
    } else if (lowerMessage.contains('party') || lowerMessage.contains('nightlife') || lowerMessage.contains('club')) {
      return _generatePartyRecommendations();
    } else if (lowerMessage.contains('bike') || lowerMessage.contains('rental') || lowerMessage.contains('transport')) {
      return _generateBikeRentalInfo();
    } else if (lowerMessage.contains('event') || lowerMessage.contains('festival')) {
      return _generateEventInfo();
    } else if (lowerMessage.contains('itinerary') || lowerMessage.contains('plan') || lowerMessage.contains('schedule')) {
      return _generateItinerary();
    } else if (lowerMessage.contains('budget') || lowerMessage.contains('cheap') || lowerMessage.contains('affordable')) {
      return _generateBudgetPlan();
    } else if (lowerMessage.contains('language')) {
      return _handleLanguageChange(message);
    } else {
      return _generateGeneralResponse();
    }
  }

  String _generateDevotionalRecommendations() {
    List<dynamic> devotionalSpots = _pondyData['attractions']['devotional'];
    StringBuffer response = StringBuffer();
    
    response.writeln('🕉️ Here are some spiritual places in Pondicherry:');
    response.writeln();
    
    for (var spot in devotionalSpots) {
      response.writeln('📍 ${spot['name']}');
      response.writeln('   ${spot['description']}');
      response.writeln('   Location: ${spot['location']}');
      response.writeln('   Best time: ${spot['best_time']}');
      response.writeln('   Story: ${spot['story']}');
      response.writeln('   Current crowd: ${spot['crowd_level']}');
      response.writeln();
    }
    
    response.writeln('Would you like me to create a spiritual itinerary for you? 🙏');
    return response.toString();
  }

  String _generateAdventureRecommendations() {
    List<dynamic> adventureSpots = _pondyData['attractions']['adventure'];
    StringBuffer response = StringBuffer();
    
    response.writeln('🏄‍♂️ Adventure awaits in Pondicherry!');
    response.writeln();
    
    for (var spot in adventureSpots) {
      response.writeln('🌊 ${spot['name']}');
      response.writeln('   ${spot['description']}');
      response.writeln('   Location: ${spot['location']}');
      response.writeln('   Best time: ${spot['best_time']}');
      response.writeln('   Story: ${spot['story']}');
      response.writeln('   Current crowd: ${spot['crowd_level']}');
      response.writeln();
    }
    
    response.writeln('💡 Tip: Early morning visits help avoid crowds! Would you like transportation recommendations?');
    return response.toString();
  }

  String _generatePartyRecommendations() {
    List<dynamic> partySpots = _pondyData['attractions']['party'];
    StringBuffer response = StringBuffer();
    
    response.writeln('🎉 Let\'s explore Pondy\'s nightlife!');
    response.writeln();
    
    for (var spot in partySpots) {
      response.writeln('🍹 ${spot['name']}');
      response.writeln('   ${spot['description']}');
      response.writeln('   Location: ${spot['location']}');
      response.writeln('   Best time: ${spot['best_time']}');
      response.writeln('   Story: ${spot['story']}');
      response.writeln('   Current crowd: ${spot['crowd_level']}');
      response.writeln();
    }
    
    response.writeln('🚨 Safety tip: Always travel in groups and inform someone about your plans!');
    return response.toString();
  }

  String _generateBikeRentalInfo() {
    List<dynamic> rentals = _pondyData['transport']['bike_rentals'];
    StringBuffer response = StringBuffer();
    
    response.writeln('🏍️ Bike Rental Options in Pondicherry:');
    response.writeln();
    
    for (var rental in rentals) {
      response.writeln('🚲 ${rental['name']}');
      response.writeln('   Location: ${rental['location']}');
      response.writeln('   Price: ₹${rental['price_per_day']}/day');
      response.writeln('   Available bikes: ${rental['types'].join(', ')}');
      response.writeln('   Contact: ${rental['contact']}');
      response.writeln();
    }
    
    response.writeln('📋 Required documents: Valid ID, Driving License');
    response.writeln('💡 Tip: Book in advance during peak season!');
    return response.toString();
  }

  String _generateEventInfo() {
    List<dynamic> events = _pondyData['events'];
    StringBuffer response = StringBuffer();
    
    response.writeln('🎭 Upcoming Events in Pondicherry:');
    response.writeln();
    
    for (var event in events) {
      response.writeln('🎪 ${event['name']}');
      response.writeln('   Date: ${event['date']}');
      response.writeln('   Location: ${event['location']}');
      response.writeln('   ${event['description']}');
      response.writeln();
    }
    
    response.writeln('Would you like me to add any of these events to your itinerary?');
    return response.toString();
  }

  String _generateItinerary() {
    StringBuffer response = StringBuffer();
    
    response.writeln('📅 Suggested 3-Day Pondicherry Itinerary:');
    response.writeln();
    
    response.writeln('Day 1: French Heritage 🇫🇷');
    response.writeln('• Morning: Sri Aurobindo Ashram');
    response.writeln('• Afternoon: French Quarter walk');
    response.writeln('• Evening: Promenade Beach sunset');
    response.writeln();
    
    response.writeln('Day 2: Adventure & Nature 🌊');
    response.writeln('• Morning: Paradise Beach (boat ride)');
    response.writeln('• Afternoon: Auroville exploration');
    response.writeln('• Evening: Scuba diving session');
    response.writeln();
    
    response.writeln('Day 3: Culture & Relaxation 🎭');
    response.writeln('• Morning: Local market visit');
    response.writeln('• Afternoon: Cathedral visit');
    response.writeln('• Evening: Le Club for nightlife');
    response.writeln();
    
    response.writeln('⏰ Current traffic conditions suggest starting early morning for better experience!');
    response.writeln('Would you like me to customize this based on your preferences?');
    
    return response.toString();
  }

  String _generateBudgetPlan() {
    StringBuffer response = StringBuffer();
    
    response.writeln('💰 Budget-Friendly Pondicherry Plan:');
    response.writeln();
    
    response.writeln('🏠 Accommodation (per night):');
    response.writeln('• Budget: ₹800-1500 (hostels/guesthouses)');
    response.writeln('• Mid-range: ₹2000-4000 (boutique hotels)');
    response.writeln();
    
    response.writeln('🍽️ Food (per day):');
    response.writeln('• Local eateries: ₹400-600');
    response.writeln('• Mid-range restaurants: ₹800-1200');
    response.writeln();
    
    response.writeln('🚲 Transportation:');
    response.writeln('• Bike rental: ₹250-300/day');
    response.writeln('• Auto/taxi: ₹500-800/day');
    response.writeln();
    
    response.writeln('🎫 Attractions:');
    response.writeln('• Most spiritual sites: Free');
    response.writeln('• Museums: ₹10-50');
    response.writeln('• Adventure activities: ₹500-2000');
    response.writeln();
    
    response.writeln('💡 Total budget estimate: ₹1500-3000 per day');
    response.writeln('Would you like specific money-saving tips?');
    
    return response.toString();
  }

  String _handleLanguageChange(String message) {
    return 'To change language, please use the language selector at the top. I support English, French, Tamil, Hindi, Spanish, and German! 🌍';
  }

  String _generateGeneralResponse() {
    List<String> responses = [
      'I can help you with:\n• Tourist attractions (devotional, adventure, party spots)\n• Bike rentals and transportation\n• Cultural events and festivals\n• Budget planning\n• Custom itineraries\n• Real-time crowd and traffic updates\n\nWhat interests you most?',
      'Pondicherry is beautiful! I can guide you through its French colonial charm, spiritual ashrams, pristine beaches, and vibrant culture. What aspect would you like to explore?',
      'As your travel companion, I\'m here to make your Pondicherry experience unforgettable! Tell me about your interests - adventure, spirituality, culture, or nightlife?',
    ];
    
    return responses[Random().nextInt(responses.length)];
  }

  void _scrollToBottom() {
    Future.delayed(Duration(milliseconds: 100), () {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Pondy Travel Companion'),
        backgroundColor: Color(0xFFE65100),
        elevation: 0,
        actions: [
          PopupMenuButton<String>(
            icon: Icon(Icons.language),
            onSelected: (String language) {
              setState(() {
                _selectedLanguage = language;
              });
              _sendMessage('Language changed to $_selectedLanguage');
            },
            itemBuilder: (BuildContext context) {
              return _languages.keys.map((String language) {
                return PopupMenuItem<String>(
                  value: language,
                  child: Text('$language ${language == _selectedLanguage ? '✓' : ''}'),
                );
              }).toList();
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Chat messages
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: EdgeInsets.all(16),
              itemCount: _messages.length + (_isTyping ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == _messages.length) {
                  return _buildTypingIndicator();
                }
                return _buildMessageBubble(_messages[index]);
              },
            ),
          ),
          
          // Input area
          Container(
            padding: EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.grey.withOpacity(0.2),
                  spreadRadius: 1,
                  blurRadius: 5,
                  offset: Offset(0, -2),
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: InputDecoration(
                      hintText: 'Ask me about Pondicherry...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(25),
                        borderSide: BorderSide.none,
                      ),
                      filled: true,
                      fillColor: Colors.grey[100],
                      contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                    ),
                    onSubmitted: _sendMessage,
                  ),
                ),
                SizedBox(width: 8),
                FloatingActionButton(
                  onPressed: () => _sendMessage(_messageController.text),
                  child: Icon(Icons.send),
                  mini: true,
                  backgroundColor: Color(0xFFE65100),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(ChatMessage message) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: message.isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          if (!message.isUser)
            CircleAvatar(
              radius: 16,
              backgroundColor: Color(0xFFE65100),
              child: Text('P', style: TextStyle(color: Colors.white, fontSize: 12)),
            ),
          if (!message.isUser) SizedBox(width: 8),
          
          Flexible(
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              decoration: BoxDecoration(
                color: message.isUser ? Color(0xFFE65100) : Colors.grey[200],
                borderRadius: BorderRadius.circular(20),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    message.text,
                    style: TextStyle(
                      color: message.isUser ? Colors.white : Colors.black87,
                      fontSize: 16,
                    ),
                  ),
                  SizedBox(height: 4),
                  Text(
                    '${message.timestamp.hour}:${message.timestamp.minute.toString().padLeft(2, '0')}',
                    style: TextStyle(
                      color: message.isUser ? Colors.white70 : Colors.grey[600],
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          ),
          
          if (message.isUser) SizedBox(width: 8),
          if (message.isUser)
            CircleAvatar(
              radius: 16,
              backgroundColor: Colors.blue,
              child: Icon(Icons.person, size: 16, color: Colors.white),
            ),
        ],
      ),
    );
  }

  Widget _buildTypingIndicator() {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          CircleAvatar(
            radius: 16,
            backgroundColor: Color(0xFFE65100),
            child: Text('P', style: TextStyle(color: Colors.white, fontSize: 12)),
          ),
          SizedBox(width: 8),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            decoration: BoxDecoration(
              color: Colors.grey[200],
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              _getLocalizedText('thinking'),
              style: TextStyle(
                color: Colors.black87,
                fontSize: 16,
                fontStyle: FontStyle.italic,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;

  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
  });
}
