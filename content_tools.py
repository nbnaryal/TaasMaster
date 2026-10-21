# Text for the three tracker pages. On English pages this appears as a section below your app;
# on Nepali pages it is the page itself, with a button that opens the app.

TOOLS = {"en": {}, "ne": {}}

TOOLS["en"]["cb_tool"] = dict(
    title="Call Break Score Calculator – Free Online Call Break Score Tracker",
    desc="Track Call Break bids, tricks and totals for 4 players, with point-based or fixed-pot money mode and a who-pays-whom settlement. Works offline and saves mid-game.",
    h1="Call Break Score Tracker & Settlement",
    lede="Keep score at the table: enter each player's bid and tricks, and the tracker totals the points, ranks the players and works out who pays whom.",
    app_name="Call Break Score Tracker",
    body="""
<h3>What it does</h3>
<ul>
  <li><strong>Bids and tricks for every round.</strong> Total tricks must equal 13, so a slip at the table can't spoil the totals.</li>
  <li><strong>Automatic scoring.</strong> Make your bid and score the bid plus 0.1 for each extra trick; miss it and lose the bid.</li>
  <li><strong>Money mode.</strong> Point-based (each point is worth a set amount) or fixed pot by final place, including the double penalty for a negative total.</li>
  <li><strong>Settle up.</strong> A who-pays-whom list with the fewest possible transfers, which you can mark as paid.</li>
  <li><strong>Many games.</strong> Name each game, keep its history, export to CSV, and carry on another day.</li>
</ul>
""",
)
TOOLS["en"]["mar_tool"] = dict(
    title="Marriage Card Game Point Calculator – Free Online Score Tracker",
    desc="Calculate Marriage card game points in seconds: maal calculator for tiplu, poplu, jhiplu, alter and man, seen/unseen payments, dublee, and who pays whom. Works offline.",
    h1="Marriage Point Calculator & Tracker",
    lede="Mark each player seen or unseen, enter their maal and tap the winner — the calculator works out everyone's points and who pays whom.",
    app_name="Marriage Point Calculator",
    body="""
<h3>What it does</h3>
<ul>
  <li><strong>Maal calculator.</strong> Tap + / − for tiplu, poplu, jhiplu, alter, man card, tunnela and marriage, and it adds up the maal using the standard value tables.</li>
  <li><strong>Correct settlement.</strong> Each player gets (players × own maal) − total maal; unseen players count zero maal. Losers then pay the winner 3 if seen or 10 if unseen.</li>
  <li><strong>Dublee finish</strong> bonus, and every value is editable under Rules to match your group.</li>
  <li><strong>Full game record.</strong> Leaderboard, history, edit or delete any hand, players can sit out, and the dealer rotates.</li>
  <li><strong>Who pays whom</strong> at the end, with a summary you can copy to WhatsApp or Viber.</li>
</ul>
""",
)
TOOLS["en"]["tp_tool"] = dict(
    title="Teen Patti Score Tracker – Track Boot, Chaal, Pots & Settlement",
    desc="Track Teen Patti hands at the table: Show or Chaal mode, boot, blind and seen bets, automatic hand ranking, pots and an end-of-game who-pays-whom. Works offline.",
    h1="Teen Patti Tracker",
    lede="Play the cards at the table and let your phone keep the pot: boots, chaal, shows and the final settlement are tracked for every player.",
    app_name="Teen Patti Tracker",
    body="""
<h3>What it does</h3>
<ul>
  <li><strong>Two modes.</strong> Show mode for fast hands, or Chaal mode with blind, seen and packed players and the correct bet charged for each.</li>
  <li><strong>Hand ranking.</strong> Enter each player's three cards and it picks the winner, from trail down to high card. You choose whether A-2-3 or A-K-Q is the top sequence.</li>
  <li><strong>Pot checks.</strong> Boot + chaal + show always equals the pot, with optional chaal and pot limits.</li>
  <li><strong>Leaderboard and settlement,</strong> including who pays whom and a copyable summary.</li>
  <li><strong>History</strong> of every hand, with delete, and balances that recalculate automatically.</li>
</ul>
""",
)

TOOLS["ne"]["cb_tool"] = dict(
    title="कल ब्रेक स्कोर क्याल्कुलेटर – निःशुल्क अनलाइन स्कोर ट्र्याकर",
    desc="४ जनाको कल ब्रेक कल, हात र जम्मा अंक राख्नुहोस्। अंकअनुसार वा फिक्स पोट मोड, र कसले कसलाई कति तिर्ने हिसाब। अफलाइन चल्छ, बीचमा सेभ हुन्छ।",
    h1="कल ब्रेक स्कोर ट्र्याकर र हिसाब",
    lede="टेबलमै स्कोर राख्नुहोस्: हरेकको कल र जितेका हात लेख्नुहोस्, ट्र्याकरले अंक जोड्छ, क्रम मिलाउँछ र कसले कसलाई तिर्ने निकाल्छ।",
    app_name="कल ब्रेक स्कोर ट्र्याकर",
    body="""
<h3>यसले के गर्छ</h3>
<ul>
  <li><strong>हरेक राउन्डको कल र हात।</strong> जम्मा हात १३ नै हुनुपर्छ, त्यसैले गल्तीले अंक बिग्रिँदैन।</li>
  <li><strong>आफैँ अंक गन्ने।</strong> कल पुगे कल बराबर र हरेक बढी हातको ०.१; नपुगे कल बराबर घट्छ।</li>
  <li><strong>पैसाको हिसाब।</strong> अंकअनुसार (प्रति अंक निश्चित रकम) वा अन्तिम स्थानअनुसार फिक्स पोट, ऋणात्मक अंकमा दोब्बर जरिवाना सहित।</li>
  <li><strong>हिसाब मिलाउने।</strong> सबैभन्दा कम कारोबारमा कसले कसलाई तिर्ने सूची, तिरेपछि चिन्ह लगाउन मिल्ने।</li>
  <li><strong>धेरै खेल।</strong> हरेक खेलको नाम, इतिहास, CSV निर्यात, र अर्को दिन फेरि सुरु गर्न मिल्ने।</li>
</ul>
""",
)
TOOLS["ne"]["mar_tool"] = dict(
    title="म्यारिज कार्ड गेम अंक क्याल्कुलेटर – निःशुल्क माल हिसाब",
    desc="म्यारिजको हिसाब सेकेन्डमै: टिप्लु, पोप्लु, झिप्लु, अल्टर र म्यानको माल क्याल्कुलेटर, देखेको/नदेखेको शुल्क, डबली र कसले कसलाई तिर्ने। अफलाइन चल्छ।",
    h1="म्यारिज अंक क्याल्कुलेटर र ट्र्याकर",
    lede="हरेकलाई देखेको वा नदेखेको छान्नुहोस्, माल लेख्नुहोस् र विजेता थिच्नुहोस् — सबैको अंक र कसले कसलाई तिर्ने आफैँ निस्कन्छ।",
    app_name="म्यारिज अंक क्याल्कुलेटर",
    body="""
<h3>यसले के गर्छ</h3>
<ul>
  <li><strong>माल क्याल्कुलेटर।</strong> टिप्लु, पोप्लु, झिप्लु, अल्टर, म्यान, टनेला र म्यारिजका लागि + / − थिच्नुहोस्, मानक तालिकाअनुसार माल आफैँ जोडिन्छ।</li>
  <li><strong>सही हिसाब।</strong> हरेकको अंक = (खेलाडी संख्या × आफ्नो माल) − जम्मा माल; नदेखेकाको माल शून्य। हार्नेले विजेतालाई देखेको भए ३, नदेखेको भए १० तिर्छ।</li>
  <li><strong>डबली जित</strong> बोनस, र Rules मा सबै अंक आफ्नो समूहअनुसार बदल्न मिल्ने।</li>
  <li><strong>पूरा रेकर्ड।</strong> लिडरबोर्ड, इतिहास, कुनै पनि हात सच्याउन वा मेटाउन मिल्ने, खेलाडी बस्न मिल्ने, बाँड्ने पालो आफैँ सर्ने।</li>
  <li><strong>कसले कसलाई तिर्ने</strong> अन्त्यमा, WhatsApp वा Viber मा पठाउन मिल्ने सारांशसहित।</li>
</ul>
""",
)
TOOLS["ne"]["tp_tool"] = dict(
    title="तीन पत्ती स्कोर ट्र्याकर – बुट, चाल, पोट र हिसाब",
    desc="तीन पत्ती खेल्दा हिसाब फोनमै: शो वा चाल मोड, बुट, ब्लाइन्ड र सीन दाउ, हात आफैँ मिलाउने, पोट र अन्तिम हिसाब। अफलाइन चल्छ।",
    h1="तीन पत्ती ट्र्याकर",
    lede="तास टेबलमा खेल्नुहोस्, पोटको हिसाब फोनले राख्छ: बुट, चाल, शो र अन्तिम हिसाब हरेक खेलाडीको।",
    app_name="तीन पत्ती ट्र्याकर",
    body="""
<h3>यसले के गर्छ</h3>
<ul>
  <li><strong>दुई मोड।</strong> छिटो खेलका लागि शो मोड, वा ब्लाइन्ड, सीन र प्याक भएका खेलाडीसहित चाल मोड, जसमा हरेकको सही दाउ आफैँ लाग्छ।</li>
  <li><strong>हातको क्रम।</strong> हरेकका तीन पत्ती लेख्नुहोस्, ट्रायलदेखि हाई कार्डसम्म मिलाएर विजेता छान्छ। A-2-3 वा A-K-Q मध्ये कुन ठूलो भन्ने आफैँ छान्न मिल्छ।</li>
  <li><strong>पोट जाँच।</strong> बुट + चाल + शो सधैँ पोट बराबर, चाल र पोटको सीमा राख्न मिल्ने।</li>
  <li><strong>लिडरबोर्ड र हिसाब,</strong> कसले कसलाई तिर्ने र कपी गर्न मिल्ने सारांशसहित।</li>
  <li><strong>हरेक हातको इतिहास,</strong> मेटाउन मिल्ने, र हिसाब आफैँ फेरि मिल्ने।</li>
</ul>
""",
)

OPEN = {"en": "Open the tracker", "ne": "ट्र्याकर खोल्नुहोस्"}
