// advanced_chatbot_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:geolocator/geolocator.dart';
import 'dart:convert';
import 'dart:math';
import 'dart:async';

class AdvancedChatbotScreen extends StatefulWidget {
  @override
  _AdvancedChatbotScreenState createState() => _AdvancedChatbotScreenState();
}

class _AdvancedChatbotScreenState extends State<AdvancedChatbotScreen>
    with TickerProviderStateMixin {
  
  // Controllers and Core Variables
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final SpeechToText _speechToText = SpeechToText();
  final FlutterTts _flutterTts = FlutterTts();
  
  // Chatbot State
  List<ChatMessage> _messages = [];
  bool _isTyping = false;
  bool _isListening = false;
  bool _speechEnabled = false;
  String _selectedLanguage = 'English';
  
  // User Context and Preferences
  Map<String, dynamic> _userContext = {
    'name': '',
    'interests': <String>[],
    'budget_preference': 'moderate',
    'current_location': '',
    'visit_history': <String, int>{},
    'preferred_time': 'flexible',
    'group_size': 1,
    'visit_duration': 3, // days
  };
  
  // Real-time Data
  Map<String, dynamic> _realtimeData = {
    'weather': 'sunny',
    'traffic_conditions': {},
    'crowd_levels': {},
    'events_today': [],
    'special_offers': [],
  };
  
  // Advanced AI Components
  late ChatbotAI _ai;
  late ConversationManager _conversationManager;
  late PersonalizationEngine _personalizationEngine;
  
  // Animation Controllers
  late AnimationController _typingAnimationController;
  late AnimationController _messageAnimationController;
  
  @override
  void initState() {
    super.initState();
    _initializeChatbot();
    _initializeAnimations();
    _initializeSpeech();
    _initializeTTS();
  }

  void _initializeChatbot() async {
    _ai = ChatbotAI();
    _conversationManager = ConversationManager();
    _personalizationEngine = PersonalizationEngine();
    
    // Load user preferences
    await _loadUserPreferences();
    
    // Initialize with welcome message
    await Future.delayed(Duration(milliseconds: 500));
    _addMessage(_ai.generateWelcomeMessage(_userContext), false);
    
    // Start real-time data updates
    _startRealtimeUpdates();
  }

  void _initializeAnimations() {
    _typingAnimationController = AnimationController(
      duration: Duration(seconds: 1),
      vsync: this,
    )..repeat();
    
    _messageAnimationController = AnimationController(
      duration: Duration(milliseconds: 300),
      vsync: this,
    );
  }

  void _initializeSpeech() async {
    _speechEnabled = await _speechToText.initialize();
    setState(() {});
  }

  void _initializeTTS() async {
    await _flutterTts.setLanguage(_getLanguageCode(_selectedLanguage));
    await _flutterTts.setSpeechRate(0.7);
    await _flutterTts.setVolume(0.8);
    await _flutterTts.setPitch(1.0);
  }

  void _startRealtimeUpdates() {
    // Simulate real-time data updates every 30 seconds
    Timer.periodic(Duration(seconds: 30), (timer) {
      _updateRealtimeData();
    });
  }

  void _updateRealtimeData() {
    setState(() {
      _realtimeData['crowd_levels'] = _generateCrowdData();
      _realtimeData['traffic_conditions'] = _generateTrafficData();
      _realtimeData['weather'] = _getCurrentWeather();
    });
  }

  Map<String, String> _generateCrowdData() {
    List<String> levels = ['low', 'moderate', 'high'];
    Random random = Random();
    return {
      'Sri Aurobindo Ashram': levels[random.nextInt(3)],
      'Promenade Beach': levels[random.nextInt(3)],
      'Paradise Beach': levels[random.nextInt(3)],
      'French Quarter': levels[random.nextInt(3)],
    };
  }

  Map<String, String> _generateTrafficData() {
    List<String> conditions = ['light', 'moderate', 'heavy'];
    Random random = Random();
    return {
      'Mission Street': conditions[random.nextInt(3)],
      'MG Road': conditions[random.nextInt(3)],
      'ECR': conditions[random.nextInt(3)],
    };
  }

  String _getCurrentWeather() {
    List<String> weather = ['sunny', 'cloudy', 'rainy', 'windy'];
    return weather[Random().nextInt(weather.length)];
  }

  Future<void> _loadUserPreferences() async {
    // In production, load from SharedPreferences or API
    // For demo, use default values
    setState(() {
      _userContext['interests'] = ['culture', 'adventure'];
      _userContext['budget_preference'] = 'moderate';
    });
  }

  void _addMessage(String text, bool isUser) {
    setState(() {
      _messages.add(ChatMessage(
        text: text,
        isUser: isUser,
        timestamp: DateTime.now(),
        messageId: _generateMessageId(),
      ));
    });
    
    _messageAnimationController.forward().then((_) {
      _messageAnimationController.reset();
    });
    
    _scrollToBottom();
    
    if (!isUser) {
      _speakMessage(text);
    }
  }

  String _generateMessageId() {
    return 'msg_${DateTime.now().millisecondsSinceEpoch}_${Random().nextInt(1000)}';
  }

  void _sendMessage(String text) {
    if (text.trim().isEmpty) return;

    _addMessage(text, true);
    _messageController.clear();

    // Update conversation context
    _conversationManager.addUserMessage(text);
    
    setState(() {
      _isTyping = true;
    });

    // Process with advanced AI
    _processAdvancedMessage(text);
  }

  Future<void> _processAdvancedMessage(String message) async {
    try {
      // Enhanced message processing
      final response = await _ai.generateResponse(
        message: message,
        context: _userContext,
        conversationHistory: _conversationManager.getRecentHistory(),
        realtimeData: _realtimeData,
      );

      // Add delay for natural conversation flow
      await Future.delayed(Duration(milliseconds: 1500 + Random().nextInt(1000)));

      setState(() {
        _isTyping = false;
      });

      _addMessage(response.text, false);

      // Handle special actions
      if (response.actions.isNotEmpty) {
        _handleBotActions(response.actions);
      }

      // Update user preferences based on conversation
      _personalizationEngine.updatePreferences(_userContext, message, response);

    } catch (e) {
      setState(() {
        _isTyping = false;
      });
      _addMessage("I apologize, but I'm having trouble processing that right now. Could you please try again?", false);
    }
  }

  void _handleBotActions(List<BotAction> actions) {
    for (BotAction action in actions) {
      switch (action.type) {
        case 'show_map':
          _showLocationOnMap(action.data['location']);
          break;
        case 'create_itinerary':
          _createItinerary(action.data);
          break;
        case 'show_weather':
          _showWeatherInfo();
          break;
        case 'book_reminder':
          _setReminder(action.data);
          break;
      }
    }
  }

  void _showLocationOnMap(String location) {
    // Implementation for showing location on map
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Opening map for $location...')),
    );
  }

  void _createItinerary(Map<String, dynamic> data) {
    // Implementation for creating itinerary
    _showItineraryDialog(data);
  }

  void _showWeatherInfo() {
    _addMessage(
      "Current weather in Pondicherry: ${_realtimeData['weather']} 🌤️\n"
      "Perfect for outdoor activities! Would you like weather-specific recommendations?",
      false
    );
  }

  void _setReminder(Map<String, dynamic> data) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Reminder set for ${data['title']}')),
    );
  }

  void _showItineraryDialog(Map<String, dynamic> itinerary) {
    showDialog(
      context: context,
      builder: (context) => ItineraryDialog(itinerary: itinerary),
    );
  }

  void _startListening() async {
    if (!_speechEnabled) return;

    setState(() {
      _isListening = true;
    });

    await _speechToText.listen(
      onResult: (result) {
        if (result.finalResult) {
          _messageController.text = result.recognizedWords;
          setState(() {
            _isListening = false;
          });
        }
      },
      listenFor: Duration(seconds: 30),
      pauseFor: Duration(seconds: 3),
    );
  }

  void _stopListening() async {
    await _speechToText.stop();
    setState(() {
      _isListening = false;
    });
  }

  void _speakMessage(String text) async {
    // Remove special characters and emojis for better TTS
    String cleanText = text.replaceAll(RegExp(r'[^\w\s.,!?]'), '');
    await _flutterTts.speak(cleanText);
  }

  String _getLanguageCode(String language) {
    Map<String, String> codes = {
      'English': 'en-US',
      'French': 'fr-FR',
      'Tamil': 'ta-IN',
      'Hindi': 'hi-IN',
      'Spanish': 'es-ES',
      'German': 'de-DE',
    };
    return codes[language] ?? 'en-US';
  }

  void _changeLanguage(String newLanguage) async {
    setState(() {
      _selectedLanguage = newLanguage;
    });
    
    await _flutterTts.setLanguage(_getLanguageCode(newLanguage));
    
    _addMessage(
      _ai.getLocalizedMessage('language_changed', newLanguage),
      false
    );
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _typingAnimationController.dispose();
    _messageAnimationController.dispose();
    _speechToText.stop();
    _flutterTts.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _buildAppBar(),
      body: _buildBody(),
      bottomNavigationBar: _buildInputArea(),
    );
  }

  PreferredSizeWidget _buildAppBar() {
    return AppBar(
      title: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Pondy AI Companion', style: TextStyle(fontSize: 18)),
          Text(
            'Powered by Advanced AI • $_selectedLanguage',
            style: TextStyle(fontSize: 12, color: Colors.white70),
          ),
        ],
      ),
      backgroundColor: Color(0xFFE65100),
      elevation: 0,
      actions: [
        IconButton(
          icon: Icon(Icons.language),
          onPressed: _showLanguageSelector,
        ),
        IconButton(
          icon: Icon(Icons.settings),
          onPressed: _showSettingsDialog,
        ),
      ],
    );
  }

  Widget _buildBody() {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFFE65100).withOpacity(0.1), Colors.white],
          stops: [0.0, 0.3],
        ),
      ),
      child: Column(
        children: [
          _buildStatusBar(),
          Expanded(
            child: _buildMessageList(),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusBar() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.blue.withOpacity(0.1),
        border: Border(bottom: BorderSide(color: Colors.blue.withOpacity(0.3))),
      ),
      child: Row(
        children: [
          Icon(Icons.wb_sunny, size: 16, color: Colors.orange),
          SizedBox(width: 4),
          Text(
            'Weather: ${_realtimeData['weather']}',
            style: TextStyle(fontSize: 12, color: Colors.black87),
          ),
          Spacer(),
          Icon(Icons.traffic, size: 16, color: Colors.red),
          SizedBox(width: 4),
          Text(
            'Traffic: Moderate',
            style: TextStyle(fontSize: 12, color: Colors.black87),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageList() {
    return ListView.builder(
      controller: _scrollController,
      padding: EdgeInsets.all(16),
      itemCount: _messages.length + (_isTyping ? 1 : 0),
      itemBuilder: (context, index) {
        if (index == _messages.length) {
          return _buildTypingIndicator();
        }
        return _buildAnimatedMessage(_messages[index], index);
      },
    );
  }

  Widget _buildAnimatedMessage(ChatMessage message, int index) {
    return FadeTransition(
      opacity: _messageAnimationController,
      child: SlideTransition(
        position: Tween<Offset>(
          begin: Offset(message.isUser ? 1.0 : -1.0, 0.0),
          end: Offset.zero,
        ).animate(CurvedAnimation(
          parent: _messageAnimationController,
          curve: Curves.easeOut,
        )),
        child: _buildMessageBubble(message),
      ),
    );
  }

  Widget _buildMessageBubble(ChatMessage message) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: message.isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          if (!message.isUser) _buildBotAvatar(),
          if (!message.isUser) SizedBox(width: 12),
          
          Flexible(
            child: Container(
              constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: message.isUser ? Color(0xFFE65100) : Colors.grey[200],
                borderRadius: BorderRadius.circular(20).copyWith(
                  bottomLeft: Radius.circular(message.isUser ? 20 : 4),
                  bottomRight: Radius.circular(message.isUser ? 4 : 20),
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    spreadRadius: 1,
                    blurRadius: 3,
                    offset: Offset(0, 1),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    message.text,
                    style: TextStyle(
                      color: message.isUser ? Colors.white : Colors.black87,
                      fontSize: 16,
                      height: 1.3,
                    ),
                  ),
                  SizedBox(height: 6),
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        _formatTime(message.timestamp),
                        style: TextStyle(
                          color: message.isUser ? Colors.white70 : Colors.grey[600],
                          fontSize: 11,
                        ),
                      ),
                      if (!message.isUser) ...[
                        SizedBox(width: 8),
                        GestureDetector(
                          onTap: () => _speakMessage(message.text),
                          child: Icon(
                            Icons.volume_up,
                            size: 14,
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    ],
                  ),
                ],
              ),
            ),
          ),
          
          if (message.isUser) SizedBox(width: 12),
          if (message.isUser) _buildUserAvatar(),
        ],
      ),
    );
  }

  Widget _buildBotAvatar() {
    return Container(
      width: 36,
      height: 36,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Color(0xFFE65100), Color(0xFFFF9800)],
        ),
        borderRadius: BorderRadius.circular(18),
      ),
      child: Icon(
        Icons.smart_toy,
        color: Colors.white,
        size: 20,
      ),
    );
  }

  Widget _buildUserAvatar() {
    return Container(
      width: 36,
      height: 36,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.blue, Colors.lightBlue],
        ),
        borderRadius: BorderRadius.circular(18),
      ),
      child: Icon(
        Icons.person,
        color: Colors.white,
        size: 20,
      ),
    );
  }

  Widget _buildTypingIndicator() {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          _buildBotAvatar(),
          SizedBox(width: 12),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.grey[200],
              borderRadius: BorderRadius.circular(20).copyWith(
                bottomLeft: Radius.circular(4),
              ),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildTypingDot(0),
                SizedBox(width: 4),
                _buildTypingDot(1),
                SizedBox(width: 4),
                _buildTypingDot(2),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTypingDot(int index) {
    return AnimatedBuilder(
      animation: _typingAnimationController,
      builder: (context, child) {
        double value = (_typingAnimationController.value + index * 0.33) % 1.0;
        return Transform.translate(
          offset: Offset(0, -10 * (value < 0.5 ? 2 * value : 2 * (1 - value))),
          child: Container(
            width: 8,
            height: 8,
            decoration: BoxDecoration(
              color: Colors.grey[400],
              borderRadius: BorderRadius.circular(4),
            ),
          ),
        );
      },
    );
  }

  Widget _buildInputArea() {
    return Container(
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
      child: SafeArea(
        child: Row(
          children: [
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.grey[100],
                  borderRadius: BorderRadius.circular(25),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _messageController,
                        decoration: InputDecoration(
                          hintText: 'Ask me about Pondicherry...',
                          border: InputBorder.none,
                          contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                        ),
                        onSubmitted: _sendMessage,
                        textCapitalization: TextCapitalization.sentences,
                      ),
                    ),
                    if (_speechEnabled)
                      GestureDetector(
                        onTap: _isListening ? _stopListening : _startListening,
                        child: Container(
                          padding: EdgeInsets.all(8),
                          child: Icon(
                            _isListening ? Icons.mic : Icons.mic_none,
                            color: _isListening ? Colors.red : Colors.grey[600],
                            size: 24,
                          ),
                        ),
                      ),
                  ],
                ),
              ),
            ),
            SizedBox(width: 12),
            GestureDetector(
              onTap: () => _sendMessage(_messageController.text),
              child: Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [Color(0xFFE65100), Color(0xFFFF9800)],
                  ),
                  borderRadius: BorderRadius.circular(24),
                ),
                child: Icon(
                  Icons.send,
                  color: Colors.white,
                  size: 24,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showLanguageSelector() {
    showModalBottomSheet(
      context: context,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => LanguageSelectorSheet(
        currentLanguage: _selectedLanguage,
        onLanguageSelected: _changeLanguage,
      ),
    );
  }

  void _showSettingsDialog() {
    showDialog(
      context: context,
      builder: (context) => SettingsDialog(
        userContext: _userContext,
        onSettingsChanged: (newContext) {
          setState(() {
            _userContext = newContext;
          });
        },
      ),
    );
  }

  String _formatTime(DateTime dateTime) {
    return '${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
  }
}

// Supporting Classes

class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final String messageId;

  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
    required this.messageId,
  });
}

class ChatbotAI {
  Map<String, List<String>> _responseTemplates = {
    'welcome': [
      'Bonjour! Welcome to the beautiful union territory of Pondicherry! 🌺 I\'m your AI travel companion, ready to help you explore this French colonial paradise.',
      'Namaste and Bonjour! I\'m thrilled you\'re here in Pondicherry! 🙏 Let me be your personal guide to discover the perfect blend of Indian spirituality and French elegance.',
    ],
    'devotional': [
      'Pondicherry is a spiritual haven! Let me guide you through sacred spaces that will touch your soul.',
      'The spiritual energy here is incredible! I can recommend ashrams, temples, and meditation centers perfect for your journey.',
    ],
    'adventure': [
      'Ready for some excitement? Pondicherry offers amazing water sports, beach adventures, and thrilling experiences!',
      'Adventure awaits! From scuba diving to parasailing, let\'s plan your adrenaline-filled itinerary.',
    ],
    'culture': [
      'The rich Franco-Tamil culture here is fascinating! Let me show you the best museums, galleries, and cultural sites.',
      'Dive into 300 years of French colonial history mixed with Tamil traditions - it\'s absolutely unique!',
    ],
  };

  Future<AIResponse> generateResponse({
    required String message,
    required Map<String, dynamic> context,
    required List<String> conversationHistory,
    required Map<String, dynamic> realtimeData,
  }) async {
    // Simulate AI processing time
    await Future.delayed(Duration(milliseconds: 800));

    String intent = _classifyIntent(message);
    String response = _generateContextualResponse(intent, message, context, realtimeData);
    List<BotAction> actions = _generateActions(intent, message, context);

    return AIResponse(
      text: response,
      intent: intent,
      confidence: 0.85,
      actions: actions,
    );
  }

  String _classifyIntent(String message) {
    String lower = message.toLowerCase();
    
    if (_containsKeywords(lower, ['temple', 'spiritual', 'ashram', 'meditation', 'prayer'])) {
      return 'devotional';
    } else if (_containsKeywords(lower, ['adventure', 'beach', 'diving', 'sports', 'exciting'])) {
      return 'adventure';
    } else if (_containsKeywords(lower, ['culture', 'museum', 'history', 'french', 'colonial'])) {
      return 'culture';
    } else if (_containsKeywords(lower, ['food', 'restaurant', 'eat', 'cuisine', 'dining'])) {
      return 'food';
    } else if (_containsKeywords(lower, ['bike', 'rental', 'transport', 'travel'])) {
      return 'transport';
    } else if (_containsKeywords(lower, ['itinerary', 'plan', 'schedule', 'trip'])) {
      return 'itinerary';
    } else if (_containsKeywords(lower, ['budget', 'cost', 'price', 'cheap', 'expensive'])) {
      return 'budget';
    } else if (_containsKeywords(lower, ['weather', 'rain', 'sunny', 'climate'])) {
      return 'weather';
    } else {
      return 'general';
    }
  }

  bool _containsKeywords(String text, List<String> keywords) {
    return keywords.any((keyword) => text.contains(keyword));
  }

  String _generateContextualResponse(String intent, String message, Map<String, dynamic> context, Map<String, dynamic> realtimeData) {
    switch (intent) {
      case 'devotional':
        return _generateDevotionalResponse(context, realtimeData);
      case 'adventure':
        return _generateAdventureResponse(context, realtimeData);
      case 'culture':
        return _generateCultureResponse(context, realtimeData);
      case 'food':
        return _generateFoodResponse(context, realtimeData);
      case 'transport':
        return _generateTransportResponse(context, realtimeData);
      case 'weather':
        return _generateWeatherResponse(realtimeData);
      case 'budget':
        return _generateBudgetResponse(context);
      case 'itinerary':
        return _generateItineraryResponse(context, realtimeData);
      default:
        return _generateGeneralResponse(context);
    }
  }

  String _generateDevotionalResponse(Map<String, dynamic> context, Map<String, dynamic> realtimeData) {
    List<String> responses = [
      '🕉️ For spiritual seekers like yourself, I recommend starting with the Sri Aurobindo Ashram - the spiritual heart of Pondicherry. The current crowd level is ${realtimeData['crowd_levels']?['Sri Aurobindo Ashram'] ?? 'moderate'}.',
      '🙏 The divine energy here is palpable! Visit the Mother\'s Temple for morning meditation, then explore the peaceful Matrimandir in nearby Auroville. Perfect for your spiritual journey!',
      '✨ Pondicherry\'s spiritual landscape is extraordinary! The Manakula Vinayagar Temple by the beach offers a unique Tamil spiritual experience, while the ashrams provide French-influenced meditation practices.',
    ];
    
    String response = responses[Random().nextInt(responses.length)];
    
    // Add personalized recommendations based on time
    int hour = DateTime.now().hour;
    if (hour < 10) {
      response += '\n\n🌅 Since it\'s morning, this is perfect timing for ashram visits and meditation sessions!';
    } else if (hour > 17) {
      response += '\n\n🌆 Evening aarti ceremonies are particularly beautiful at local temples.';
    }
    
    return response;
  }

  String _generateAdventureResponse(Map<String, dynamic> context, Map<String, dynamic> realtimeData) {
    return '🏄‍♂️ Adventure time! Based on current conditions:\n\n'
           '🌊 Paradise Beach: Perfect for water sports (crowd level: ${realtimeData['crowd_levels']?['Paradise Beach'] ?? 'moderate'})\n'
           '🤿 Scuba diving at Temple Adventures\n'
           '🚴‍♂️ Cycling tour through French Quarter\n'
           '🌅 Sunrise kayaking in the backwaters\n\n'
           '💡 Pro tip: Early morning adventures have fewer crowds and better weather!';
  }

  String _generateCultureResponse(Map<String, dynamic> context, Map<String, dynamic> realtimeData) {
    return '🏛️ Pondicherry\'s Franco-Tamil culture is absolutely fascinating!\n\n'
           '🇫🇷 French Quarter highlights:\n'
           '• French Institute for exhibitions\n'
           '• Notre Dame Cathedral\n'
           '• Colonial architecture walking tour\n\n'
           '🎭 Cultural experiences:\n'
           '• Traditional Tamil performances\n'
           '• French cuisine cooking classes\n'
           '• Local artisan workshops\n\n'
           'Current crowd at French Quarter: ${realtimeData['crowd_levels']?['French Quarter'] ?? 'moderate'}';
  }

  String _generateFoodResponse(Map<String, dynamic> context, Map<String, dynamic> realtimeData) {
    String budgetLevel = context['budget_preference'] ?? 'moderate';
    
    if (budgetLevel == 'budget') {
      return '🍽️ Delicious budget-friendly options:\n\n'
             '• Surguru Restaurant - Authentic South Indian (₹100-250)\n'
             '• Hot Breads - Fresh bakery items (₹50-150)\n'
             '• Local street food at Goubert Market\n\n'
             '🥘 Don\'t miss the unique Pondicherry fusion cuisine!';
    } else if (budgetLevel == 'luxury') {
      return '🍾 Premium dining experiences:\n\n'
             '• Villa Shanti - Fine dining French cuisine\n'
             '• Le Dupleix - Colonial elegance with fusion menu\n'
             '• Palais de Mahe - Royal dining experience\n\n'
             '✨ Perfect for a memorable culinary journey!';
    } else {
      return '🍛 Wonderful mid-range dining options:\n\n'
             '• Cafe des Arts - French-Tamil fusion\n'
             '• Tanto - Italian with local ingredients\n'
             '• Indian Coffee House - Historic charm\n\n'
             '🌶️ Mix of traditional Tamil and French colonial flavors!';
    }
  }

  String _generateTransportResponse(Map<String, dynamic> context, Map<String, dynamic> realtimeData) {
    return '🏍️ Getting around Pondicherry:\n\n'
           '🚲 **Recommended: Bike Rental**\n'
           '• French Quarter Bikes: ₹250/day\n'
           '• Pondy Bike Rentals: ₹300/day (premium bikes)\n\n'
           '🚗 **Alternatives:**\n'
           '• Auto rickshaws: ₹10-15/km\n'
           '• Taxi services: ₹12-18/km\n\n'
           '📱 **Apps:** Ola, Uber available\n\n'
           'Current traffic on MG Road: ${realtimeData['traffic_conditions']?['MG Road'] ?? 'moderate'}\n'
           '💡 Tip: Bikes give you the freedom to explore narrow French Quarter lanes!';
  }

  String _generateWeatherResponse(Map<String, dynamic> realtimeData) {
    String weather = realtimeData['weather'] ?? 'sunny';
    
    Map<String, String> weatherAdvice = {
      'sunny': '☀️ Beautiful sunny weather! Perfect for beach visits and outdoor exploration. Don\'t forget sunscreen!',
      'cloudy': '⛅ Nice cloudy weather - ideal for walking tours and sightseeing without harsh sun.',
      'rainy': '🌧️ Monsoon vibes! Great time for indoor cultural sites, cafes, and ashram meditation sessions.',
      'windy': '💨 Breezy conditions - perfect for water sports and beachside activities!',
    };
    
    return 'Current weather: $weather\n\n${weatherAdvice[weather] ?? 'Check local weather for updates.'}';
  }

  String _generateBudgetResponse(Map<String, dynamic> context) {
    return '💰 Smart budget planning for Pondicherry:\n\n'
           '🏠 **Accommodation (per night):**\n'
           '• Budget: ₹800-1500 (hostels/guesthouses)\n'
           '• Mid-range: ₹2000-4000 (boutique hotels)\n'
           '• Luxury: ₹5000+ (heritage properties)\n\n'
           '🍽️ **Food (per day):**\n'
           '• Street food/local: ₹300-500\n'
           '• Restaurants: ₹800-1200\n'
           '• Fine dining: ₹2000+\n\n'
           '🚲 **Transport:** ₹250-300 (bike rental)\n'
           '🎫 **Attractions:** Most temples free, museums ₹10-50\n\n'
           '💡 **Money-saving tips:**\n'
           '• Visit during off-season (June-September)\n'
           '• Try local eateries\n'
           '• Walk in French Quarter (it\'s small!)';
  }

  String _generateItineraryResponse(Map<String, dynamic> context, Map<String, dynamic> realtimeData) {
    int days = context['visit_duration'] ?? 3;
    List<String> interests = List<String>.from(context['interests'] ?? ['culture']);
    
    return '📅 Perfect ${days}-day itinerary for you:\n\n'
           '**Day 1: French Colonial Heritage** 🇫🇷\n'
           '• 9 AM: Sri Aurobindo Ashram\n'
           '• 11 AM: French Quarter walking tour\n'
           '• 2 PM: Pondicherry Museum\n'
           '• 5 PM: Promenade Beach sunset\n\n'
           '**Day 2: Adventure & Nature** 🌊\n'
           '• 8 AM: Paradise Beach (boat ride)\n'
           '• 1 PM: Auroville exploration\n'
           '• 4 PM: Scuba diving session\n\n'
           '**Day 3: Culture & Relaxation** 🎭\n'
           '• 9 AM: Local market visit\n'
           '• 11 AM: Cathedral and churches\n'
           '• 3 PM: Handicraft shopping\n'
           '• 7 PM: Traditional dinner\n\n'
           '🚦 Real-time tip: Current traffic is ${realtimeData['traffic_conditions']?['MG Road'] ?? 'moderate'} - plan accordingly!';
  }

  String _generateGeneralResponse(Map<String, dynamic> context) {
    List<String> responses = [
      'I\'m here to make your Pondicherry experience unforgettable! What would you like to explore? 🌺\n\n'
      '• 🕉️ Spiritual ashrams and temples\n'
      '• 🏄‍♂️ Beach adventures and water sports\n'
      '• 🏛️ French colonial culture and history\n'
      '• 🍽️ Fusion cuisine experiences\n'
      '• 🚲 Transportation and local tips',
      
      'Pondicherry is a magical blend of cultures! Tell me what interests you most:\n\n'
      '✨ Spiritual journeys and meditation\n'
      '🌊 Coastal adventures and beaches\n'
      '🎭 Cultural heritage and art\n'
      '🍜 Local cuisine and dining\n'
      '📍 Personalized itinerary planning',
    ];
    
    return responses[Random().nextInt(responses.length)];
  }

  List<BotAction> _generateActions(String intent, String message, Map<String, dynamic> context) {
    List<BotAction> actions = [];
    
    switch (intent) {
      case 'devotional':
        actions.add(BotAction(type: 'show_map', data: {'location': 'Sri Aurobindo Ashram'}));
        break;
      case 'adventure':
        actions.add(BotAction(type: 'show_map', data: {'location': 'Paradise Beach'}));
        break;
      case 'itinerary':
        actions.add(BotAction(type: 'create_itinerary', data: context));
        break;
      case 'weather':
        actions.add(BotAction(type: 'show_weather', data: {}));
        break;
    }
    
    return actions;
  }

  String generateWelcomeMessage(Map<String, dynamic> context) {
    List<String> welcomeMessages = _responseTemplates['welcome']!;
    String base = welcomeMessages[Random().nextInt(welcomeMessages.length)];
    
    String name = context['name'] ?? '';
    if (name.isNotEmpty) {
      base = base.replaceFirst('Welcome', 'Welcome, $name,');
    }
    
    return base + '\n\nWhat would you like to explore today?';
  }

  String getLocalizedMessage(String key, String language) {
    Map<String, Map<String, String>> localizedMessages = {
      'language_changed': {
        'English': 'Great! I\'ve switched to English. How can I help you explore Pondicherry?',
        'French': 'Parfait! J\'ai basculé en français. Comment puis-je vous aider à explorer Pondichéry?',
        'Tamil': 'சிறப்பு! நான் தமிழுக்கு மாறிவிட்டேன். பாண்டிச்சேரியை ஆராய நான் எப்படி உதவ முடியும்?',
        'Hindi': 'बहुत बढ़िया! मैं हिंदी में स्विच हो गया हूं। मैं आपको पांडिचेरी एक्सप्लोर करने में कैसे मदद कर सकता हूं?',
      },
    };
    
    return localizedMessages[key]?[language] ?? 
           localizedMessages[key]?['English'] ?? 
           'Message not available';
  }
}

class AIResponse {
  final String text;
  final String intent;
  final double confidence;
  final List<BotAction> actions;

  AIResponse({
    required this.text,
    required this.intent,
    required this.confidence,
    required this.actions,
  });
}

class BotAction {
  final String type;
  final Map<String, dynamic> data;

  BotAction({required this.type, required this.data});
}

class ConversationManager {
  List<String> _conversationHistory = [];
  
  void addUserMessage(String message) {
    _conversationHistory.add('User: $message');
    if (_conversationHistory.length > 10) {
      _conversationHistory.removeAt(0);
    }
  }
  
  void addBotMessage(String message) {
    _conversationHistory.add('Bot: $message');
    if (_conversationHistory.length > 10) {
      _conversationHistory.removeAt(0);
    }
  }
  
  List<String> getRecentHistory() {
    return List.from(_conversationHistory);
  }
}

class PersonalizationEngine {
  void updatePreferences(Map<String, dynamic> context, String userMessage, AIResponse response) {
    // Update user interests based on conversation
    String intent = response.intent;
    
    List<String> interests = List<String>.from(context['interests'] ?? []);
    if (!interests.contains(intent) && intent != 'general') {
      interests.add(intent);
      context['interests'] = interests.take(5).toList(); // Keep top 5 interests
    }
    
    // Update visit history
    Map<String, int> visitHistory = Map<String, int>.from(context['visit_history'] ?? {});
    visitHistory[intent] = (visitHistory[intent] ?? 0) + 1;
    context['visit_history'] = visitHistory;
  }
}

// UI Components

class LanguageSelectorSheet extends StatelessWidget {
  final String currentLanguage;
  final Function(String) onLanguageSelected;

  const LanguageSelectorSheet({
    Key? key,
    required this.currentLanguage,
    required this.onLanguageSelected,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final languages = [
      {'name': 'English', 'flag': '🇺🇸', 'native': 'English'},
      {'name': 'French', 'flag': '🇫🇷', 'native': 'Français'},
      {'name': 'Tamil', 'flag': '🇮🇳', 'native': 'தமிழ்'},
      {'name': 'Hindi', 'flag': '🇮🇳', 'native': 'हिंदी'},
      {'name': 'Spanish', 'flag': '🇪🇸', 'native': 'Español'},
      {'name': 'German', 'flag': '🇩🇪', 'native': 'Deutsch'},
    ];

    return Container(
      padding: EdgeInsets.all(20),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 40,
            height: 4,
            decoration: BoxDecoration(
              color: Colors.grey[300],
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          SizedBox(height: 20),
          Text(
            'Choose Language',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 20),
          ...languages.map((lang) => ListTile(
            leading: Text(lang['flag']!, style: TextStyle(fontSize: 24)),
            title: Text(lang['name']!),
            subtitle: Text(lang['native']!),
            trailing: currentLanguage == lang['name'] 
                ? Icon(Icons.check, color: Color(0xFFE65100))
                : null,
            onTap: () {
              onLanguageSelected(lang['name']!);
              Navigator.pop(context);
            },
          )).toList(),
          SizedBox(height: 20),
        ],
      ),
    );
  }
}

class SettingsDialog extends StatefulWidget {
  final Map<String, dynamic> userContext;
  final Function(Map<String, dynamic>) onSettingsChanged;

  const SettingsDialog({
    Key? key,
    required this.userContext,
    required this.onSettingsChanged,
  }) : super(key: key);

  @override
  _SettingsDialogState createState() => _SettingsDialogState();
}

class _SettingsDialogState extends State<SettingsDialog> {
  late Map<String, dynamic> _context;
  final TextEditingController _nameController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _context = Map.from(widget.userContext);
    _nameController.text = _context['name'] ?? '';
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Personalization Settings'),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: _nameController,
              decoration: InputDecoration(
                labelText: 'Your Name',
                border: OutlineInputBorder(),
              ),
              onChanged: (value) {
                _context['name'] = value;
              },
            ),
            SizedBox(height: 16),
            
            Text('Interests:', style: TextStyle(fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Wrap(
              spacing: 8,
              children: [
                'devotional', 'adventure', 'culture', 'food', 'nightlife'
              ].map((interest) => FilterChip(
                label: Text(interest.capitalize()),
                selected: (_context['interests'] as List<String>? ?? []).contains(interest),
                onSelected: (selected) {
                  setState(() {
                    List<String> interests = List<String>.from(_context['interests'] ?? []);
                    if (selected) {
                      interests.add(interest);
                    } else {
                      interests.remove(interest);
                    }
                    _context['interests'] = interests;
                  });
                },
              )).toList(),
            ),
            
            SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _context['budget_preference'] ?? 'moderate',
              decoration: InputDecoration(
                labelText: 'Budget Preference',
                border: OutlineInputBorder(),
              ),
              items: [
                DropdownMenuItem(value: 'budget', child: Text('Budget (₹1000-2000/day)')),
                DropdownMenuItem(value: 'moderate', child: Text('Moderate (₹2000-4000/day)')),
                DropdownMenuItem(value: 'luxury', child: Text('Luxury (₹4000+/day)')),
              ],
              onChanged: (value) {
                setState(() {
                  _context['budget_preference'] = value;
                });
              },
            ),
            
            SizedBox(height: 16),
            Row(
              children: [
                Text('Visit Duration: '),
                Expanded(
                  child: Slider(
                    value: (_context['visit_duration'] ?? 3).toDouble(),
                    min: 1,
                    max: 14,
                    divisions: 13,
                    label: '${(_context['visit_duration'] ?? 3)} days',
                    onChanged: (value) {
                      setState(() {
                        _context['visit_duration'] = value.round();
                      });
                    },
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: () {
            widget.onSettingsChanged(_context);
            Navigator.pop(context);
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: Color(0xFFE65100),
          ),
          child: Text('Save'),
        ),
      ],
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }
}

class ItineraryDialog extends StatelessWidget {
  final Map<String, dynamic> itinerary;

  const ItineraryDialog({Key? key, required this.itinerary}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        padding: EdgeInsets.all(20),
        constraints: BoxConstraints(maxHeight: MediaQuery.of(context).size.height * 0.8),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Your Personalized Itinerary',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                IconButton(
                  onPressed: () => Navigator.pop(context),
                  icon: Icon(Icons.close),
                ),
              ],
            ),
            Divider(),
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildItineraryContent(),
                  ],
                ),
              ),
            ),
            SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton.icon(
                  onPressed: () {
                    // Share itinerary functionality
                    _shareItinerary();
                  },
                  icon: Icon(Icons.share),
                  label: Text('Share'),
                ),
                ElevatedButton.icon(
                  onPressed: () {
                    // Save itinerary functionality
                    _saveItinerary();
                  },
                  icon: Icon(Icons.save),
                  label: Text('Save'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFFE65100),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildItineraryContent() {
    return Column(
      children: [
        ListTile(
          leading: Icon(Icons.access_time, color: Color(0xFFE65100)),
          title: Text('Duration: ${itinerary['duration'] ?? '3'} days'),
          subtitle: Text('Estimated budget: ₹${itinerary['budget'] ?? '6000'}'),
        ),
        
        ...List.generate(3, (index) {
          int day = index + 1;
          return ExpansionTile(
            leading: CircleAvatar(
              backgroundColor: Color(0xFFE65100),
              child: Text('$day', style: TextStyle(color: Colors.white)),
            ),
            title: Text('Day $day: Cultural Heritage'),
            children: [
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  children: [
                    _buildTimelineItem('9:00 AM', 'Sri Aurobindo Ashram', 'Spiritual exploration'),
                    _buildTimelineItem('11:30 AM', 'French Quarter Walk', 'Colonial architecture'),
                    _buildTimelineItem('2:00 PM', 'Local cuisine lunch', 'French-Tamil fusion'),
                    _buildTimelineItem('5:00 PM', 'Promenade Beach', 'Sunset viewing'),
                  ],
                ),
              ),
            ],
          );
        }),
      ],
    );
  }

  Widget _buildTimelineItem(String time, String activity, String description) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Container(
            width: 60,
            child: Text(time, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
          ),
          Container(
            width: 8,
            height: 8,
            decoration: BoxDecoration(
              color: Color(0xFFE65100),
              shape: BoxShape.circle,
            ),
          ),
          SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(activity, style: TextStyle(fontWeight: FontWeight.w500)),
                Text(description, style: TextStyle(color: Colors.grey[600], fontSize: 12)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _shareItinerary() {
    // Implement share functionality
    print('Sharing itinerary...');
  }

  void _saveItinerary() {
    // Implement save functionality
    print('Saving itinerary...');
  }
}

// Extension for string capitalization
extension StringCapitalization on String {
  String capitalize() {
    if (isEmpty) return this;
    return '${this[0].toUpperCase()}${substring(1)}';
  }
}
