# English page content. {link:key} placeholders are replaced with the localized URL of that page.

PAGES = {}

PAGES["home"] = dict(
    title="TaasMaster – Free Call Break, Marriage & Teen Patti Score Tracker",
    desc="Free score trackers for Nepali card games: Call Break, Marriage and Teen Patti. Works offline on your phone and saves scores automatically. No sign-up.",
    h1="Keep score. Keep playing.",
    lede="Score Call Break, Marriage and Teen Patti on your phone. It does the maths and settles up at the end of the night.",
    body="""
<ul class="sheet">
  <li><a href="{link:cb_tool}"><span class="pip" aria-hidden="true">♠</span><span class="name">Call Break</span><span class="what">Bids, tricks, money mode and who pays whom.</span><span class="scribble" aria-hidden="true">3.2 &nbsp;−4 &nbsp;6.1</span></a></li>
  <li><a href="{link:mar_tool}"><span class="pip red" aria-hidden="true">♥</span><span class="name">Marriage</span><span class="what">Maal calculator, seen and unseen, final settlement.</span><span class="scribble" aria-hidden="true">+37 &nbsp;−21</span></a></li>
  <li><a href="{link:tp_tool}"><span class="pip" aria-hidden="true">♣</span><span class="name">Teen Patti</span><span class="what">Boot, chaal, shows and the pot for every hand.</span><span class="scribble" aria-hidden="true">A A A</span></a></li>
</ul>
<p class="note">Tap a game, add the players, and keep playing. Scores save on your phone after every hand, and the trackers keep working without internet.</p>
<h2>Learn the rules</h2>
<ul class="plain">
  <li><a href="{link:cb_rules}">Call Break rules, scoring and bidding strategy</a></li>
  <li><a href="{link:mar_rules}">Marriage rules: maal, tiplu, jokers and settlement</a></li>
  <li><a href="{link:tp_rules}">Teen Patti hand rankings and variations</a></li>
  <li><a href="{link:faq}">Questions people ask at the table</a></li>
</ul>
<h2>Made for the table</h2>
<ul>
  <li><strong>Works offline.</strong> Install it once and it keeps going through load-shedding and weak signal.</li>
  <li><strong>Never loses a game.</strong> A refresh, a closed tab or a flat battery doesn't wipe the scores.</li>
  <li><strong>One-handed.</strong> Big buttons, nothing to sign up for, and no ads mid-hand.</li>
  <li><strong>In Nepali too.</strong> Switch to <a href="{link_ne:home}" hreflang="ne" lang="ne" data-setlang="ne">नेपाली</a> once and every page and tracker follows.</li>
</ul>
<p class="note">TaasMaster records scores and settlements for games you play in person. It doesn't take bets, hold money or process payments.</p>
""",
)

PAGES["cb_rules"] = dict(
    title="Call Break Rules, Scoring & Bidding Strategy – Complete Guide",
    desc="Complete Call Break card game rules: dealing, calling (bidding), spades as trump, how scoring works with worked examples, house rules and bidding strategy tips.",
    h1="Call Break Rules, Scoring and Strategy",
    lede="Call Break is a four-player trick-taking game with spades as permanent trumps. Here is everything you need to play — and to score it correctly.",
    body="""
<p class="callout">Keeping score? Open the <a href="{link:cb_tool}">Call Break score tracker</a> — it does the maths for you.</p>
<h2>Players and cards</h2>
<p>Four players each play for themselves with a standard 52-card deck. Cards rank A (high), K, Q, J, 10 down to 2. <strong>Spades are always trumps.</strong> A game is usually <strong>5 rounds</strong> (deals), and the deal passes to the right after each round.</p>
<h2>Dealing</h2>
<p>The dealer shuffles and deals all 52 cards, one at a time, so everyone holds 13. Many groups allow a redeal if a player has no spades, or no card higher than a 10 — agree on this before you start.</p>
<h2>Calling (bidding)</h2>
<p>Starting with the player to the dealer's right, each player calls the number of tricks they expect to win, from <strong>1 to 13</strong>. Each player calls once; there is no raising. The calls do not need to add up to 13 — they usually don't.</p>
<h2>Playing the tricks</h2>
<ul>
  <li>The player to the dealer's right leads the first trick. The winner of each trick leads the next.</li>
  <li>You <strong>must follow suit</strong> if you can.</li>
  <li>In most Nepali games you must also <strong>try to win</strong> the trick: if you can beat the highest card played so far, you must.</li>
  <li>If you can't follow suit, you must play a spade (trump) if you have one — and beat an earlier spade if you can.</li>
  <li>If you have neither the led suit nor a spade, play any card.</li>
  <li>The highest spade wins the trick; if no spade was played, the highest card of the suit led wins.</li>
</ul>
<h2>How scoring works</h2>
<p>After all 13 tricks:</p>
<ul>
  <li><strong>Made your call</strong> (won at least as many tricks as you called): score your call, plus 0.1 for each extra trick.</li>
  <li><strong>Missed your call</strong>: lose points equal to your call.</li>
</ul>
<div class="table-wrap"><table>
<thead><tr><th>Call</th><th>Tricks won</th><th class="num">Score</th></tr></thead>
<tbody>
<tr><td>3</td><td>3</td><td class="num">3</td></tr>
<tr><td>3</td><td>5</td><td class="num">3.2</td></tr>
<tr><td>4</td><td>2</td><td class="num">−4</td></tr>
<tr><td>6</td><td>9</td><td class="num">6.3</td></tr>
</tbody></table></div>
<p>Scores are added up over the rounds. After the last round, the player with the highest total wins.</p>
<h2>Common house rules</h2>
<ul>
  <li><strong>Big call bonus:</strong> some groups give 13 points to a player who calls 8 or more and makes it.</li>
  <li><strong>Maximum call:</strong> some groups cap calls at 8.</li>
  <li><strong>Number of rounds:</strong> 5 is standard, but you can set any number in the tracker.</li>
</ul>
<h2>Bidding strategy</h2>
<ul>
  <li><strong>Count sure winners first.</strong> The ace of spades is a certain trick. Side-suit aces usually win, especially in suits where you hold only two or three cards.</li>
  <li><strong>Long spades are worth tricks.</strong> With five or more spades, your lower spades often win once others run out.</li>
  <li><strong>Shortness is power.</strong> A void or a single card in a side suit lets you trump early — count roughly one trick per spare spade you can use this way.</li>
  <li><strong>Kings and queens are shaky.</strong> A king without its ace is a coin flip; a lone queen rarely wins. Value them cautiously.</li>
  <li><strong>Missing costs more than overshooting.</strong> Missing a call of 5 costs 10 points of swing compared with making it; an extra trick only gives 0.1. When in doubt, call one less.</li>
  <li><strong>Use your position.</strong> The last player to call knows the total so far. If the calls already add up to 13 or more, tricks will be fought for — call conservatively.</li>
  <li><strong>Mind the scoreboard.</strong> In the last round, a player who is behind may need to call aggressively; a leader can call safely.</li>
</ul>
""",
    faq=[
        ("How is Call Break scored?", "If you win at least as many tricks as you called, you score your call plus 0.1 for each extra trick. If you win fewer, you lose points equal to your call. For example, call 4 and win 5 scores 4.1; call 4 and win 3 scores −4."),
        ("How many rounds are in a game of Call Break?", "The standard game is 5 rounds. The player with the highest total after the last round wins. Some groups play more rounds by agreement."),
        ("What is the minimum and maximum call in Call Break?", "The minimum call is 1. The maximum is 13, although some groups cap calls at 8."),
        ("Do you have to win the trick if you can in Call Break?", "In most Nepali rules, yes: you must follow suit and play a higher card if you have one, and if you can't follow suit you must trump with a spade."),
        ("What happens if a player has no spades?", "Many groups allow a redeal if any player's hand has no spades or no face cards. Agree on this rule before the game starts."),
    ],
)

PAGES["mar_rules"] = dict(
    title="Marriage Card Game Rules – Maal, Tiplu, Joker Points & Settlement",
    desc="Full Marriage card game rules: sequences, tunnela and dublee, seeing the maal, tiplu/poplu/jhiplu/alter points, how to settle at the end, and 21-card vs 31-card variants.",
    h1="Marriage Card Game Rules: Maal, Tiplu and Settlement",
    lede="Marriage is Nepal's favourite rummy-style game, played with three decks and 21 cards each. This guide covers play, maal points and how to settle up.",
    body="""
<p class="callout">Settling a hand? The <a href="{link:mar_tool}">Marriage point calculator</a> works out every payment for you.</p>
<p class="note">Marriage rules vary a lot between families and groups. Below are the most common rules — agree on anything you play differently before dealing.</p>
<h2>Players and cards</h2>
<p>Marriage is played by <strong>2 to 5 players</strong> (some groups play with 6) using <strong>three standard 52-card decks</strong> shuffled together. Some groups add printed jokers (often called <em>man</em> cards). Each player is dealt <strong>21 cards</strong>. The rest form the draw pile, and one card is turned face up to start the discard pile.</p>
<h2>The sets</h2>
<ul>
  <li><strong>Sequence:</strong> three or more cards in a row of the same suit, e.g. 5♥ 6♥ 7♥.</li>
  <li><strong>Pure sequence:</strong> a sequence made without any joker.</li>
  <li><strong>Trial:</strong> three cards of the same rank in different suits, e.g. 9♠ 9♥ 9♦.</li>
  <li><strong>Tunnela:</strong> three identical cards — same rank and same suit, e.g. three K♣. A tunnela counts as a pure set.</li>
  <li><strong>Dublee:</strong> a pair of identical cards (same rank and suit).</li>
</ul>
<h2>Turns</h2>
<p>On your turn, draw one card — from the draw pile or the top of the discard pile — then discard one card. You always hold 21 cards between turns.</p>
<h2>Seeing the maal</h2>
<p>Before jokers count for you, you must <strong>"see" the maal</strong>. To do that, you show <strong>three pure sets</strong> (pure sequences or tunnelas) on your turn. You then look at the hidden <strong>tiplu</strong> card (the cut joker) and can use jokers from then on.</p>
<p>Alternatively, a player can take the <strong>dublee route</strong>: show seven dublees to see the maal, and finish with an eighth dublee.</p>
<h2>Tiplu and the jokers</h2>
<p>Once the tiplu is revealed, these cards become jokers (wild cards):</p>
<ul>
  <li><strong>Tiplu:</strong> same rank and suit as the cut card. With three decks there are three tiplus.</li>
  <li><strong>Poplu:</strong> one rank above the tiplu, same suit.</li>
  <li><strong>Jhiplu:</strong> one rank below the tiplu, same suit.</li>
  <li><strong>Alter:</strong> same rank and same colour as the tiplu, different suit.</li>
  <li><strong>Ordinary jokers:</strong> same rank as the tiplu in the other-colour suits. Wild, but worth no points.</li>
</ul>
<p>Example: if the tiplu is 6♥, then 7♥ is poplu, 5♥ is jhiplu, 6♦ is alter, and 6♠ and 6♣ are ordinary jokers.</p>
<h2>How maal points work</h2>
<p>Maal is the points value of the jokers and special sets you hold. Two or three copies of the same maal card are worth more than the single value added up. These are the standard values the Marriage calculator uses:</p>
<div class="table-wrap"><table>
<thead><tr><th>Maal</th><th class="num">1 card</th><th class="num">2 cards</th><th class="num">3 cards</th><th class="num">Tunnela</th></tr></thead>
<tbody>
<tr><td>Marriage (jhiplu + tiplu + poplu)</td><td class="num">10</td><td class="num">30</td><td class="num">—</td><td class="num">—</td></tr>
<tr><td>Tiplu</td><td class="num">3</td><td class="num">8</td><td class="num">—</td><td class="num">—</td></tr>
<tr><td>Poplu / Jhiplu</td><td class="num">2</td><td class="num">5</td><td class="num">10</td><td class="num">15</td></tr>
<tr><td>Alter</td><td class="num">5</td><td class="num">15</td><td class="num">25</td><td class="num">35</td></tr>
<tr><td>Man (printed joker)</td><td class="num">5</td><td class="num">15</td><td class="num">25</td><td class="num">45</td></tr>
<tr><td>Ordinary tunnela</td><td class="num" colspan="4">5 each</td></tr>
<tr><td>Ordinary-joker tunnela</td><td class="num" colspan="4">10 each</td></tr>
</tbody></table></div>
<p>With three decks there are only three copies of any card, so a player can hold at most three of each, and a card used in a marriage can't be counted again on its own. Sources and families differ on a few values (two tiplus are 7 in some rules, a poplu tunnela 20), so agree on yours before the game; every value can be changed in the calculator's Rules settings.</p>
<h2>Finishing a hand</h2>
<p>A player who has seen the maal wins the hand by arranging all their cards into valid sets (jokers allowed) and making a final discard. Everyone then shows their hand and counts their maal. Only players who have seen the maal can count theirs.</p>
<h2>How to settle at the end</h2>
<ol>
  <li><strong>Add up the total maal</strong> of every player who has seen. Players who haven't seen count as zero.</li>
  <li><strong>Each player's maal result</strong> = their maal × number of players − total maal. A positive number means they collect; negative means they pay.</li>
  <li><strong>Losers pay the winner a fee:</strong> commonly 3 points from each player who saw the maal and 10 points from each player who did not.</li>
  <li><strong>Dublee finish:</strong> when the winner finishes with 8 dublees, many groups add a bonus (often 5 points) from each player, usually only when 4 or more are playing.</li>
</ol>
<h3>Worked example</h3>
<p>Four players. Asha wins with 8 maal. Bikash saw and has 3 maal. Chandra saw and has 0. Dipa never saw the maal. Total maal = 8 + 3 + 0 = 11.</p>
<div class="table-wrap"><table>
<thead><tr><th>Player</th><th class="num">Maal result</th><th class="num">Fee</th><th class="num">Net</th></tr></thead>
<tbody>
<tr><td>Asha (winner)</td><td class="num">8×4 − 11 = +21</td><td class="num">+16</td><td class="num">+37</td></tr>
<tr><td>Bikash (seen)</td><td class="num">3×4 − 11 = +1</td><td class="num">−3</td><td class="num">−2</td></tr>
<tr><td>Chandra (seen)</td><td class="num">0×4 − 11 = −11</td><td class="num">−3</td><td class="num">−14</td></tr>
<tr><td>Dipa (unseen)</td><td class="num">−11</td><td class="num">−10</td><td class="num">−21</td></tr>
</tbody></table></div>
<p>The nets always add up to zero. Over a session, keep a running total and settle once at the end — the calculator's <em>Settle up</em> button shows the fewest transfers needed.</p>
<h2>Kidnap and Murder variants</h2>
<ul>
  <li><strong>Kidnap:</strong> a player who hasn't seen the maal loses their joker points to the winner.</li>
  <li><strong>Murder:</strong> a player who hasn't seen the maal loses their joker points, but they don't go to the winner.</li>
</ul>
<h2>21-card vs 31-card Marriage</h2>
<p><strong>21-card Marriage</strong> is the standard game described on this page: three decks, 21 cards each, three pure sets to see the maal, seven sets to finish.</p>
<p><strong>31-card Marriage</strong> is a longer house variant with bigger hands, so hands take more turns and more sets must be built to finish. Because its details change from group to group, agree on these before you deal: how many decks, how many pure sets are needed to see the maal, whether the dublee route is allowed and how many dublees it needs, and the maal values. Settlement works exactly the same way, so the calculator handles both versions.</p>
""",
    faq=[
        ("How many points is a tiplu worth in Marriage?", "In the most common rules a tiplu is worth 3 maal points, and poplu and jhiplu are worth 2 each. A marriage (jhiplu, tiplu and poplu together) is worth 10."),
        ("What does it mean to see the maal?", "Seeing the maal means showing three pure sets (pure sequences or tunnelas) so you can look at the tiplu card. Only players who have seen the maal can use jokers and count their maal points."),
        ("How much does an unseen player pay in Marriage?", "Commonly, each player who did not see the maal pays the winner 10 points, and each player who saw pays 3. Unseen players also count zero maal."),
        ("How do you calculate Marriage points at the end of a hand?", "Add up the maal of everyone who has seen. Each player's result is their maal times the number of players, minus the total maal. Then each loser pays the winner the seen or unseen fee."),
        ("What is a dublee in Marriage?", "A dublee is a pair of identical cards of the same rank and suit. Seven dublees let you see the maal, and an eighth dublee finishes the game."),
    ],
)

PAGES["tp_rules"] = dict(
    title="Teen Patti Rules & Hand Rankings – Variations Explained",
    desc="Teen Patti hand rankings from trail to high card, how ties are decided, how a round is played, and popular variations like Muflis, AK47 and Joker.",
    h1="Teen Patti Rules and Hand Rankings",
    lede="Teen Patti (three cards) is a quick South Asian card game. This page covers the rules and hand rankings only.",
    body="""
<p class="callout">Keeping track of points? Use the <a href="{link:tp_tool}">Teen Patti points tracker</a>.</p>
<h2>The basics</h2>
<p>Teen Patti is played by 3 to 6 players (sometimes more) with one 52-card deck and no printed jokers. Each player gets <strong>three cards</strong> face down. Aces are high, except in the A-2-3 sequence.</p>
<h2>Hand rankings (highest to lowest)</h2>
<div class="table-wrap"><table>
<thead><tr><th>#</th><th>Hand</th><th>What it is</th><th>Example</th></tr></thead>
<tbody>
<tr><td>1</td><td><strong>Trail</strong> (trio, set)</td><td>Three cards of the same rank</td><td>A♠ A♥ A♦</td></tr>
<tr><td>2</td><td><strong>Pure sequence</strong> (straight flush)</td><td>Three cards in a row, same suit</td><td>Q♥ K♥ A♥</td></tr>
<tr><td>3</td><td><strong>Sequence</strong> (run)</td><td>Three cards in a row, mixed suits</td><td>4♣ 5♦ 6♠</td></tr>
<tr><td>4</td><td><strong>Color</strong> (flush)</td><td>Three cards of the same suit, not in a row</td><td>2♦ 8♦ J♦</td></tr>
<tr><td>5</td><td><strong>Pair</strong></td><td>Two cards of the same rank</td><td>10♠ 10♣ 7♥</td></tr>
<tr><td>6</td><td><strong>High card</strong></td><td>None of the above</td><td>K♠ 9♦ 4♣</td></tr>
</tbody></table></div>
<h2>Breaking ties</h2>
<ul>
  <li><strong>Trail:</strong> higher rank wins — A-A-A is the best hand, 2-2-2 the lowest trail.</li>
  <li><strong>Sequences:</strong> A-K-Q is the highest, then A-2-3 (in most rules), then K-Q-J, down to 4-3-2.</li>
  <li><strong>Color and high card:</strong> compare the highest card, then the second, then the third.</li>
  <li><strong>Pair:</strong> the higher pair wins; if pairs are equal, the higher odd card wins.</li>
  <li>In a show or side show, if the two hands are exactly equal, the player who asked for it usually loses. In a showdown where nobody asked, equal hands split the pot.</li>
</ul>
<h2>How a round is played</h2>
<ol>
  <li>Everyone puts a fixed starting amount (the <em>boot</em>) into the pot, then three cards are dealt to each player.</li>
  <li>Players can play <strong>blind</strong> (without looking at their cards) or <strong>seen</strong> (after looking). A blind player's stake is half that of a seen player.</li>
  <li>Going round the table, each player either stays in by matching the current stake or folds (<em>packs</em>).</li>
  <li>A seen player can ask the previous seen player for a <strong>side show</strong> — a private comparison where the weaker hand must fold. The other player may refuse.</li>
  <li>When only two players remain, either can ask for a <strong>show</strong>: both reveal and the better hand wins the pot.</li>
</ol>
<h2>Popular variations</h2>
<ul>
  <li><strong>Muflis (lowball):</strong> rankings are reversed — the lowest hand wins.</li>
  <li><strong>AK47:</strong> all aces, kings, fours and sevens are jokers (wild cards).</li>
  <li><strong>Joker:</strong> one card is turned up after the deal; all cards of that rank are wild.</li>
  <li><strong>Lowest joker:</strong> the lowest card in each player's hand is wild for that player.</li>
  <li><strong>Four-card (best of four):</strong> each player gets four cards and plays the best three.</li>
</ul>
<p class="note">TaasMaster only records the game you play in person. It doesn't take bets, hold money or process payments.</p>
""",
    faq=[
        ("What is the highest hand in Teen Patti?", "A trail (three of a kind) is the highest hand, and three aces is the best trail. Next comes a pure sequence, then a sequence, color, pair and high card."),
        ("Is A-2-3 higher than K-Q-J in Teen Patti?", "In most rules, yes. A-K-Q is the highest sequence, A-2-3 is second, and K-Q-J is third."),
        ("Which is higher in Teen Patti, a sequence or a color?", "A sequence (three cards in a row) beats a color (three cards of the same suit that are not in a row)."),
        ("What is Muflis in Teen Patti?", "Muflis is a variation where the hand rankings are reversed, so the lowest hand wins."),
        ("What happens when two Teen Patti hands are equal?", "In a show or side show the player who asked for it usually loses a tie. Otherwise equal hands split the pot."),
    ],
)

PAGES["faq"] = dict(
    title="Card Game FAQ – Call Break, Marriage & Teen Patti Questions Answered",
    desc="Answers to the questions players ask most about Call Break scoring, Marriage maal and settlement, Teen Patti hands, and using the TaasMaster score trackers offline.",
    h1="Frequently Asked Questions",
    lede="Quick answers to the questions that come up most at the table.",
    body="""
<p>Can't find your question? Each game also has a full guide: <a href="{link:cb_rules}">Call Break rules</a>, <a href="{link:mar_rules}">Marriage rules</a> and <a href="{link:tp_rules}">Teen Patti rules</a>.</p>
""",
    faq=[
        ("Does TaasMaster work without internet?", "Yes. After your first visit, the site is stored on your phone and works offline — handy during load-shedding or when mobile data is weak."),
        ("How do I install TaasMaster on my phone?", "On Android (Chrome), tap the Install button at the top or choose 'Add to Home screen' from the menu. On iPhone (Safari), tap Share and then 'Add to Home Screen'."),
        ("Will I lose my scores if I refresh the page?", "No. Scores are saved on your phone after every change, so a refresh, closed tab or restart keeps the game. Every game stays saved, with its history, until you delete it."),
        ("Are my scores uploaded anywhere?", "No. Everything stays in your phone's browser storage. Nothing is sent to a server, and there is no account."),
        ("Can two phones share the same game?", "Not yet — each phone keeps its own game. Pick one scorekeeper per table."),
        ("How is Call Break scored with extra tricks?", "Each extra trick above your call adds 0.1. Call 3 and win 5, and you score 3.2. Winning fewer than your call loses your call."),
        ("How many points does an unseen player pay in Marriage?", "In common rules, each unseen player pays the winner 10 points and each seen player pays 3. You can change these values in the calculator's Rules settings."),
        ("What happens if nobody else saw the maal in Marriage?", "Then only the winner's maal counts. The winner collects their maal points from each other player, plus the unseen fee (commonly 10) from each of them."),
        ("Does TaasMaster handle money or payments?", "No. The trackers only record amounts and show who owes whom at the end. Any settling up happens between players; the site never takes bets, holds money or processes payments."),
        ("Is TaasMaster free?", "Yes, completely free, with no sign-up."),
    ],
)
