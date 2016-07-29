# coding=utf-8

#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
import unittest
import traceback

import cld2, cld2full

VERBOSE = False

fr_en_Latn = 'France is the largest country in Western Europe and the third-largest in Europe as a whole. A accès aux chiens et aux frontaux qui lui ont été il peut consulter et modifier ses collections et exporter Cet article concerne le pays européen aujourd’hui appelé République française. Pour d’autres usages du nom France, Pour une aide rapide et effective, veuiller trouver votre aide dans le menu ci-dessus. Motoring events began soon after the construction of the first successful gasoline-fueled automobiles. The quick brown fox jumped over the lazy dog'

testData = (
  ('ENGLISH', 'confiscation of goods is assigned as the penalty part most of the courts consist of members and when it is necessary to bring public cases before a jury of members two courts combine for the purpose the most important cases of all are brought jurors or'),
  ('ARMENIAN', ' ա յ եվ նա հիացած աչքերով նայում է հինգհարկանի շենքի տարօրինակ փոքրիկ քառակուսի պատուհաններին դեռ մենք շատ ենք հետամնաց ասում է նա այսպես է'),
  ('CHEROKEE', 'ᎠᎢᏍᎩ ᎠᏟᎶᏍᏗ ᏥᏄᏍᏛᎩ ᎦᎫᏍᏛᏅᎯ ᎾᎥᎢ'),
  ('DHIVEHI', ' ހިންދީ ބަހުން ވާހަކަ ދައްކާއިރު ދެވަނަ ބަހެއްގެ ގޮތުގައާއި އެނޫން ގޮތްގޮތުން ހިންދީ ބަހުން ވާހަކަ ދައްކާ މީހުންގެ އަދަދު މިލިއަނަށް'),
  ('GEORGIAN', ' ა ბირთვიდან მიღებული ელემენტი მენდელეევის პერიოდულ სიტემაში გადაინაცვლებს ორი უჯრით'),
  ('GREEK', ' ή αρνητική αναζήτηση λέξης κλειδιού καταστήστε τις μεμονωμένες λέξεις κλειδιά περισσότερο στοχοθετημένες με τη μετατροπή τους σε'),
  ('GUJARATI', ' આના પરિણામ પ્રમાણસર ફોન્ટ અવતરણ ચિન્હવાળા પાઠને છુપાવો બધા સમૂહો શોધાયા હાલનો જ સંદેશ વિષયની'),
  ('INUKTITUT', 'ᐃᑯᒪᒻᒪᑦ ᕿᓈᖏᓐᓇᓲᖑᒻᒪᑦ ᑎᑎᖅᑕᓕᒫᖅᓃᕕᑦ ᑎᑦᕆᐊᑐᓐᖏᑦᑕᑎᑦ ᑎᑎᖅᑕᑉᐱᑦ ᓯᕗᓂᖓᓂ ᑎᑎᖅᖃᖅ ᑎᑎᕆᐊᑐᓐᖏᑕᐃᑦ ᕿᓂᓲᖑᔪᒍᑦ ᑎᑎᖅᑕᓕᒫᖅᓃᕕᑦ'),
  ('KANNADA', ' ಂಠಯ್ಯನವರು ತುಮಕೂರು ಜಿಲ್ಲೆಯ ಚಿಕ್ಕನಾಯಕನಹಳ್ಳಿ ತಾಲ್ಲೂಕಿನ ತೀರ್ಥಪುರ ವೆಂಬ ಸಾಧಾರಣ ಹಳ್ಳಿಯ ಶ್ಯಾನುಭೋಗರ'),
  ('KHMER', ' ក ខ គ ឃ ង ច ឆ ជ ឈ ញ ដ ឋ ឌ ឍ ណ ត ថ ទ ធ ន ប ផ ព ភ ម យ រ ល វ ស ហ ឡ អ ឥ ឦ ឧ ឪ ឫ ឬ ឯ ឱ ទាំងអស់'),
  ('LAOTHIAN', ' ກຫາທົ່ວທັງເວັບ ແລະໃນເວັບໄຮ້ສາຍ ທຳອິດໃຫ້ທຳການຊອກຫາກ່ອນ ຈາກນັ້ນ ໃຫ້ກົດປຸ່ມເມນູ ໃນໜ້າຜົນໄດ້'),
  ('LIMBU', 'ᤁᤡᤖᤠᤳ ᤕᤠᤰᤌᤢᤱ ᤆᤢᤶᤗᤢᤱᤖᤧ ᤛᤥᤎᤢᤱᤃᤧᤴ ᤀᤡᤔᤠᤴᤛᤡᤱ ᤆᤧᤶᤈᤱᤗᤧ ᤁᤢᤔᤡᤱᤅᤥ ᤏᤠᤈᤡᤖᤡ ᤋᤱᤒᤣ ᥈᥆᥆᥉ ᤒᤠ ᤈᤏᤘᤖᤡ ᤗᤠᤏᤢᤀᤠᤱ ᤁ᤹ᤏᤠ ᤋᤱᤒᤣ ᤁᤠᤰ ᤏᤠ᤺ᤳᤋᤢ ᤕᤢᤖᤢᤒᤠ ᤀᤡᤔᤠᤴᤛᤡᤱ ᤋᤱᤃᤡᤵᤛᤡᤱ ᤌᤡᤶᤒᤣᤴ ᤂᤠᤃᤴ ᤛᤡᤛᤣ᤺ᤰᤗᤠ ᥇᥍ ᤂᤧᤴ ᤀᤡᤛᤡᤰ ᥇ ᤈᤏᤘᤖᤡ ᥈᥆᥆᥊ ᤀᤥ ᤏᤠᤛᤢᤵ ᤆᤥ᤺ᤰᤔᤠ ᤌᤡᤶᤒᤣ ᤋᤱᤃᤠᤶᤛᤡᤱᤗ ᤐᤳᤐᤠ ᤀᤡᤱᤄᤱ ᤘᤠ᤹'),
  ('MALAYALAM', ' ം അങ്ങനെ ഞങ്ങള് അവരുടെ മുമ്പില് നിന്നു ഔടും ഉടനെ നിങ്ങള് പതിയിരിപ്പില് നിന്നു എഴുന്നേറ്റു'),
  ('ORIYA', 'ଅକ୍ଟୋବର ଡିସେମ୍ବର'),
  ('PUNJABI', ' ਂ ਦਿਨਾਂ ਵਿਚ ਭਾਈ ਸਾਹਿਬ ਦੀ ਬੁੱਚੜ ਗੋਬਿੰਦ ਰਾਮ ਨਾਲ ਅੜਫਸ ਚੱਲ ਰਹੀ ਸੀ ਗੋਬਿੰਦ ਰਾਮ ਨੇ ਭਾਈ ਸਾਹਿਬ ਦੀਆਂ ਭੈਣਾ'),
  ('SINHALESE', ' අනුරාධ මිහිඳුකුල නමින් සකුරා ට ලිපියක් තැපෑලෙන් එවා තිබුණා කි ් රස්ටි ෂෙල්ටන් ප ් රනාන්දු ද'),
  ('SYRIAC', 'ܐܕܪܝܣ ܓܛܘ ܫܘܪܝܐ ܡܢ ܦܪܢܣܐ ܡܢ ܐܣܦܢܝܐ ܚܐܪܘܬܐ ܒܐܕܪ ܒܢܝܣܢ ܫܛܝܚܘܬܐ ܟܠܢܝܐ ܡܝ̈ܐ ܒܥܠܡܐ'),
  ('TAGALOG', ' ᜋᜇ᜔ ᜐᜓᜎᜆ᜔ ᜃ ᜈᜅ᜔ ᜊᜌ᜔ᜊᜌᜒᜈ᜔ ᜂᜉᜅ᜔᜔ ᜋᜐᜈᜌ᜔ ᜎᜅ᜔ ᜁᜐ ᜉᜅ᜔ ᜀᜃ᜔ᜎᜆ᜔ ᜆᜓᜅ᜔ᜃᜓᜎ᜔ ᜐ ᜊᜌ᜔ᜊᜌᜒᜈ᜔ ᜐ ᜆᜒᜅᜒᜈ᜔ ᜃᜓ'),
  ('TAMIL', ' அங்கு ராஜேந்திர சோழனால் கட்டப்பட்ட பிரம்மாண்டமான சிவன் கோவில் ஒன்றும் உள்ளது தொகு'),
  ('TELUGU', ' ఁ దనర జయించిన తత్వ మరసి చూడఁ దాన యగును రాజయోగి యిట్లు తేజరిల్లుచు నుండు విశ్వదాభిరామ వినర వేమ'),
  ('THAI', ' กฏในการค้นหา หรือหน้าเนื้อหา หากท่านเลือกลงโฆษณา ท่านอาจจะปรับต้องเพิ่มงบประมาณรายวันตา'),
  ('Chinese', '产品的简报和公告 提交该申请后无法进行更改 请确认您的选择是正确的 对于要提交的图书 我确认 我是版权所有者或已得到版权所有者的授权 要更改您的国家 地区 请在此表的最上端更改您的'),
  ('ChineseT', ' 之前為 帳單交易作業區 已變更 廣告內容 之前為 銷售代表 之前為 張貼日期為 百分比之前為 合約 為 目標對象條件已刪除 結束日期之前為'),
  ('Japanese', ' このペ ジでは アカウントに指定された予算の履歴を一覧にしています それぞれの項目には 予算額と特定期間のステ タスが表示されます 現在または今後の予算を設定するには'),
  ('Korean', ' 개별적으로 리포트 액세스 권한을 부여할 수 있습니다 액세스 권한 부여사용자에게 프로필 리포트에 액세스할 수 있는 권한을 부여하시려면 가용 프로필 상자에서 프로필 이름을 선택한 다음'),
  ('AFRIKAANS', ' aam skukuza die naam beteken hy wat skoonvee of hy wat alles onderstebo keer wysig bosveldkampe boskampe is kleiner afgeleë ruskampe wat oor min fasiliteite beskik daar is geen restaurante of winkels nie en slegs oornagbesoekers word toegelaat bateleur'),
  ('ALBANIAN', ' a do të kërkoni nga beogradi që të njohë pavarësinë e kosovës zoti thaçi prishtina është gati ta njoh pavarësinë e serbisë ndërsa natyrisht se do të kërkohet një gjë e tillë që edhe beogradi ta njoh shtetin e pavarur dhe sovran të'),
  ('ARABIC', 'احتيالية بيع أي حساب'),
  ('AZERBAIJANI', ' a az qalıb breyn rinq intellektual oyunu üzrə yarışın zona mərhələləri keçirilib miq un qalıqlarının dənizdən çıxarılması davam edir məhəmməd peyğəmbərin karikaturalarını çap edən qəzetin baş redaktoru iş otağında ölüb'),
  ('BASQUE', ' a den eraso bat honen kontra hortaz eragiketa bakarrik behar dituen eraso batek aes apurtuko luke nahiz eta oraingoz eraso bideraezina izan gaur egungo teknologiaren mugak direla eta oraingoz kezka hauek alde batera utzi daitezke orain arteko indar'),
  ('BELARUSIAN', ' а друкаваць іх не было тэхнічна магчыма бліжэй за вільню тым самым часам нямецкае кіраўніцтва прапаноўвала апроч ўвядзення лацінкі яе'),
  ('BENGALI', 'গ্যালারির ৩৮ বছর পূর্তিতে মূল্যছাড় অর্থনীতি বিএনপির ওয়াক আউট তপন চৌধুরী হারবাল অ্যাসোসিয়েশনের সভাপতি আন্তর্জাতিক পরামর্শক বোর্ড দিয়ে শরিয়াহ্ ইনন্ডেক্স করবে সিএসই মালিকপক্ষের কান্না, শ্রমিকের অনিশ্চয়তা মতিঝিলে সমাবেশ নিষিদ্ধ: এফবিসিসিআইয়ের ধন্যবাদ বিনোদন বিশেষ প্রতিবেদন বাংলালিংকের গ্র্যান্ডমাস্টার সিজন-৩ ব্রাজিলে বিশ্বকাপ ফুটবল আয়োজনবিরোধী বিক্ষোভ দেশের নিরাপত্তার  চেয়ে অনেক বেশি সচেতন । প্রার্থীদের দক্ষতা  ও যোগ্যতার পাশাপাশি তারা জাতীয় ইস্যুগুলোতে প্রাধান্য দিয়েছেন । ” পাঁচটি সিটিতে ২০ লাখ ভোটারদের দিয়ে জাতীয় নির্বাচনে ৮ কোটি ভোটারদের সঙ্গে তুলনা করা যাবে কি একজন দর্শকের এমন প্রশ্নে জবাবে আব্দুল্লাহ আল নোমান বলেন , “ এই পাঁচটি সিটি কর্পোরেশন নির্বাচন দেশের পাঁচটি বড় বিভাগের প্রতিনিধিত্ব করছে । এছাড়া এখানকার ভোটার রা সবাই সচেতন । তারা'),
  ('BIHARI', 'काल में उनका हमला से बचे खाती एहिजा भाग के अइले आ भोजपुर नाम से नगर बसवले. एकरा बारे में विस्तार से जानकारी नीचे दीहल गइल बा. बाकिर आश्चर्यजनक रूप से मालवा के राजा भोज के बिहार आवे आ भोजपुर नगर बसावे आ चाहे भोजपुरी के साथे उनकर कवनो संबंध होखे के कवनो जानकारी भोपाल के भोज संस्थान आ चाहे मध्य प्रदेश के इतिहासकार लोगन के तनिको नइखे. हालांकि ऊ सब लोग एह बात के मानत बा कि एकरा बारे में अबहीं तकले मूर्ति बनवइलें. राजा भोज के जवना जगहा पऽ वाग्देवी के दर्शन भइल रहे, ओही स्थान पऽ एह मूर्ति के स्थापना कइल गइल. अब अगर एह मंदिर के एह शिलालेख के तस्वीर (पृष्ठ संख्या 33 पऽ प्रकाशित) रउआ धेयान से देखीं तऽ एकरा पऽ कैथी लिपि में -सीताराम- लिखल साफ लउकत बा. कैथी भोजपुरी के बहुत प्रचलित लिपि रहल बिया. एकरा बारे में कवनो शंका संदेह बिहार-यूपी के जानकार लोगन में नइखे. एल. एस. एस. वो माले के लिखल पढ़ीं '),
  ('BULGARIAN', ' а дума попада в състояние на изпитание ключовите думи с предсказана малко под то изискване на страниците за търсене в'),
  ('CATALAN', 'al final en un únic lloc nhorabona l correu electrònic està concebut com a eina de productivitat aleshores per què perdre el temps arxivant missatges per després intentar recordar on els veu desar i per què heu d eliminar missatges importants per l'),
  ('CEBUANO', 'Ang Sugbo usa sa mga labing ugmad nga lalawigan sa nasod. Kini ang sentro sa komersyo, edukasyon ug industriya sa sentral ug habagatang dapit sa kapupod-an. Ang mipadayag sa Sugbo isip ikapito nga labing nindot nga pulo sa , ang nag-inusarang pulo sa Pilipinas nga napasidunggan sa maong magasin sukad pa sa tuig'),
  ('CROATIAN', 'Posljednja dva vladara su Kijaksar (Κυαξαρης; 625-585 prije Krista), fraortov sin koji će proširiti teritorij Medije i Astijag. Kijaksar je imao kćer ili unuku koja se zvala Amitis a postala je ženom Nabukodonosora II. kojoj je ovaj izgradio Viseće vrtove Babilona. Kijaksar je modernizirao svoju vojsku i uništio Ninivu 612. prije Krista. Naslijedio ga je njegov sin, posljednji medijski kralj, Astijag, kojega je detronizirao (srušio sa vlasti) njegov unuk Kir Veliki. Zemljom su zavladali Perzijanci.'),
  ('CZECH', ' a akci opakujte film uložen vykreslit gmail tokio smazat obsah adresáře nelze načíst systémový profil jednotky smoot okud používáte pro určení polokoule značky z západ nebo v východ používejte nezáporné hodnoty zeměpisné délky nelze'),
  ('DANISH', ' a z tallene og punktummer der er tilladte log ud angiv den ønskede adgangskode igen november gem personlige oplysninger kontrolspørgsmål det sidste tegn i dit brugernavn skal være et bogstav a z eller tal skriv de tegn du kan se i billedet nedenfor'),
  ('DUTCH', ' a als volgt te werk om een configuratiebestand te maken sitemap gen py ebruik filters om de s op te geven die moeten worden toegevoegd of uitgesloten op basis van de opmaaktaal elke sitemap mag alleen de s bevatten voor een bepaalde opmaaktaal dit'),
  ('ENGLISH', ' a backup credit card by visiting your billing preferences page or visit the adwords help centre for more details https adwords google com support bin answer py answer hl en we were unable to process the payment of for your outstanding google adwords'),
  ('ESTONIAN', ' a niipea kui sinu maksimaalne igakuine krediidi limiit on meie poolt heaks kiidetud on sinu kohustuseks see krediidilimiit'),
  ('FINNISH', ' a joilla olet käynyt tämä kerro meille kuka ä olet ei tunnistettavia käyttötietoja kuten virheraportteja käytetään google desktopin parantamiseen etsi näyttää mukautettuja uutisia google desktop keskivaihto leikkaa voit kaksoisnapsauttaa'),
  ('FRENCH', ' a accès aux collections et aux frontaux qui lui ont été attribués il peut consulter et modifier ses collections et exporter des configurations de collection toutefois il ne peut pas créer ni supprimer des collections enfin il a accès aux fonctions'),
  ('GALICIAN', '  debe ser como mínimo taranto tendas de venda polo miúdo cociñas servizos bordado canadá viaxes parques de vehículos de recreo hotel oriental habitación recibir unha postal no enderezo indicado anteriormente'),
  ('GANDA', ' abaana ba bani lukaaga mu ana mu babiri abaana ba bebayi lukaaga mu abiri mu basatu abaana ba azugaadi lukumi mu ebikumi bibiri mu abiri mu babiri abaana ba adonikamu lukaaga mu nltaaga mu mukaaga abaana ba biguvaayi enkumi bbiri mu ataano mu mukaaga'),
  ('GERMAN', ' abschnitt ordner aktivieren werden die ordnereinstellungen im farbabschnitt deaktiviert öchten sie wirklich fortfahren eldtypen angeben optional n diesem schritt geben sie für jedesfeld aus dem datenset den typ an ieser schritt ist optional eldtypen'),
  ('HAITIAN_CREOLE', ' ak pitit tout sosyete a chita se pou sa leta dwe pwoteje yo nimewo leta fèt pou li pwoteje tout paran ak pitit nan peyi a menm jan kit paran yo marye kit yo pa marye tout manman ki fè pitit leta fèt pou ba yo konkoul menm jan tou pou timoun piti ak pou'),
  ('HEBREW', ' או לערוך את העדפות ההפצה אנא עקוב אחרי השלבים הבאים כנס לחשבון האישי שלך ב'),
  ('HINDI', ' ं ऐडवर्ड्स विज्ञापनों के अनुभव पर आधारित हैं और इनकी मदद से आपको अपने विज्ञापनों का अधिकतम लाभ'),
  ('HMONG', ' Kuv hlub koj txawm lub ntuj yuav si ntshi nphaus los kuv tsis ua siab nkaug txawm ntiab teb yuav si ntshi nphaus los kuv tseem ua lon tsaug vim kuv hlub koj tag lub siab'),
  ('HUNGARIAN', ' a felhasználóim a google azonosító szöveget ikor látják a felhasználóim a google azonosító szöveget felhasználók a google azonosító szöveget fogják látni minden tranzakció után ha a vásárlását regisztrációját oldalunk'),
  ('ICELANDIC', ' a afköst leitarorða þinna leitarorð neikvæð leitarorð auglýsingahópa byggja upp aðallista yfir ný leitarorð fyrir auglýsingahópana og skoða ítarleg gögn um árangur leitarorða eins og samkeppni auglýsenda og leitarmagn er krafist notkun'),
  ('INDONESIAN', 'berdiri setelah pengurusnya yang berusia 83 tahun, Fayzrahman Satarov, mendeklarasikan diri sebagai nabi dan rumahnya sebagai negara Islam Satarov digambarkan sebagai mantan ulama Islam  tahun 1970-an. Pengikutnya didorong membaca manuskripnya dan kebanyakan dilarang meninggalkan tempat persembunyian bawah tanah di dasar gedung delapan lantai mereka. Jaksa membuka penyelidikan kasus kriminal pada kelompok itu dan menyatakan akan membubarkan kelompok kalau tetap melakukan kegiatan ilegal seperti mencegah anggotanya mencari bantuan medis atau pendidikan. Sampai sekarang pihak berwajib belum melakukan penangkapan meskipun polisi mencurigai adanya tindak kekerasan pada anak. Pengadilan selanjutnya akan memutuskan apakah anak-anak diizinkan tetap tinggal dengan orang tua mereka. Kazan yang berada sekitar 800 kilometer di timur Moskow merupakan wilayah Tatarstan yang'),
  ('IRISH', ' a bhfuil na focail go léir i do cheist le fáil orthu ní gá ach focail breise a chur leis na cinn a cuardaíodh cheana chun an cuardach a bheachtú nó a chúngú má chuirtear focal breise isteach aimseofar fo aicme ar leith de na torthaí a fuarthas'),
  ('ITALIAN', ' a causa di un intervento di manutenzione del sistema fino alle ore circa ora legale costa del pacifico del novembre le campagne esistenti continueranno a essere pubblicate come di consueto anche durante questo breve periodo di inattività ci scusiamo per'),
  ('JAVANESE', ' account ten server niki kalian username meniko tanpo judul cacahe account nggonanmu wes pol pesen mu wes diguwak pesenan mu wes di simpen sante wae pesenan mu wes ke kirim mbuh tekan ora pesenan e ke kethok pesenan mu wes ke kirim mbuh tekan ora pesenan'),
  ('KINYARWANDA', ' dore ibyo ukeneye kumenya ukwo watubona ibibazo byinshi abandi babaza ububonero byibibina google onjela ho izina dyikyibina kyawe onjela ho yawe mulugo kulaho ibyandiko byawe shyilaho tegula yawe tulubaka tukongeraho iyanya mishya buliko tulambula'),
  ('LATVIAN', ' a gadskārtējā izpārdošana slēpošana jāņi atlaide izmaiņas trafikā kas saistītas ar sezonas izpārdošanu speciālajām atlaidēm u c ir parastas un atslēgvārdi kas ir populāri noteiktos laika posmos šajā laikā saņems lielāku klikšķu'),
  ('LITHUANIAN', ' a išsijungia mano idėja dėl geriausio laiko po pastarųjų savo santykių pasimokiau penki dalykai be kurių negaliu gyventi mano miegamajame tu surasi ideali pora išsilavinimas aukštoji mokykla koledžas universitetas pagrindinis laipsnis metai'),
  ('MACEDONIAN', ' гласовите коалицијата на вмро дпмне како партија со најмногу освоени гласови ќе добие евра а на сметката на коализијата за македонија'),
  ('MALAY', 'pengampunan beramai-ramai supaya mereka pulang ke rumah masing-masing. Orang-orang besarnya enggan mengiktiraf sultan yang dilantik oleh Belanda sebagai Yang DiPertuan Selangor. Orang ramai pula tidak mahu menjalankan perniagaan bijih timah dengan Belanda, selagi raja yang berhak tidak ditabalkan. Perdagang yang lain dibekukan terus kerana untuk membalas jasa beliau yang membantu Belanda menentang Riau, Johor dan Selangor. Di antara tiga orang Sultan juga dipandang oleh rakyat sebagai seorang sultan yang paling gigih. 1 | 2 SULTAN Sebagai ganti Sultan Ibrahim ditabalkan Raja Muhammad iaitu Raja Muda. Walaupun baginda bukan anak isteri pertama bergelar Sultan Muhammad bersemayam di Kuala Selangor juga. Pentadbiran baginda yang lemah itu menyebabkan Kuala Selangor menjadi sarang ioleh Cina di Lukut tidak diambil tindakan, sedangkan baginda sendiri banyak berhutang kepada 1'),
  ('MALTESE', ' ata ikteb messaġġ lil indirizzi differenti billi tagħżilhom u tagħfas il buttuna ikteb żid numri tfittxijja tal kotba mur print home kotba minn pagni ghal pagna minn ghall ktieb ta aċċessa stieden habib iehor grazzi it tim tal gruppi google'),
  ('MARATHI', 'हैदराबाद  उच्चार ऐका (सहाय्य·माहिती)तेलुगू: హైదరాబాదు , उर्दू: حیدر آباد हे भारतातील आंध्र प्रदेश राज्याच्या राजधानीचे शहर आहे. हैदराबादची लोकसंख्या ७७ लाख ४० हजार ३३४ आहे. मोत्यांचे शहर अशी एकेकाळी ओळख असलेल्या या शहराला ऐतिहासिक, सांस्कृतिक आणि स्थापत्यशास्त्रीय वारसा लाभला आहे. १९९० नंतर शिक्षण आणि माहिती तंत्रज्ञान त्याचप्रमाणे औषधनिर्मिती आणि जैवतंत्रज्ञान क्षेत्रातील उद्योगधंद्यांची वाढ शहरात झाली. दक्षिण मध्य भारतातील पर्यटन आणि तेलुगू चित्रपटनिर्मितीचे हैदराबाद हे केंद्र आहे'),
  ('NEPALI', 'अरू ठाऊँबाटपनि खुलेको छ यो खाता अर अरू ठाऊँबाटपनि खुलेको छ यो खाता अर ू'),
  ('NORWEGIAN', ' a er obligatorisk tidsforskyvning plassering av katalogsøk planinformasjon loggfilbane gruppenavn kontoinformasjon passord domene gruppeinformasjon alle kampanjesporing alternativ bruker grupper oppgaveplanlegger oppgavehistorikk kontosammendrag antall'),
  ('PERSIAN', ' آب خوردن عجله می کردند به جای باز ی کتک کاری می کردند و همه چيز مثل قبل بود فقط من ماندم و يک دنيا حرف و انتظار تا عاقبت رسيد احضاريه ی ای با'),
  ('POLISH', ' a australii będzie widział inne reklamy niż użytkownik z kanady kierowanie geograficzne sprawia że reklamy są lepiej dopasowane do użytkownika twojej strony oznacza to także że możesz nie zobaczyć wszystkich reklam które są wyświetlane na'),
  ('PORTUGUESE', ' a abit prevê que a entrada desses produtos estrangeiros no mercado têxtil e vestuário do brasil possa reduzir os preços em cerca de a partir de má notícia para os empresários que terão que lutar para garantir suas margens de lucro mas boa notícia'),
  ('ROMANIAN', ' a anunţurilor reţineţi nu plătiţi pentru clicuri sau impresii ci numai atunci când pe site ul dvs survine o acţiune dorită site urile negative nu pot avea uri de destinaţie daţi instrucţiuni societăţii dvs bancare sau constructoare să'),
  ('ROMANIAN', 'оперативэ а органелор ши институциилор екзекутиве ши а органелор жудичиаре але путерий де стат фиекэруй орган ал путерий де стат и се'),
  ('RUSSIAN', ' а неправильный формат идентификатора дн назад'),
  ('SCOTS_GAELIC', ' air son is gum bi casg air a h uile briosgaid no gum faigh thu brath nuair a tha briosgaid a tighinn gad rannsachadh ghoogle gu ceart mura bheil briosgaidean ceadaichte cuiridh google briosgaid dha do neach cleachdaidh fa leth tha google a cleachdadh'),
  ('SERBIAN', 'балчак балчак на мапи србије уреди демографија у насељу балчак живи пунолетна становника а просечна старост становништва износи година'),
  ('SERBIAN', 'Društvo | četvrtak 1.08.2013 | 13:43 Krade se i izvorska voda Izvor:  Gornji Milanovac -- U gružanskom selu Belo Polje prošle noći ukradeno je više od 10.000 litara kojima je obijen bazen. Bazen je bio zaključan i propisno obezbeđen.'),
  ('SLOVAK', ' a aktivovať reklamnú kampaň ak chcete kampaň pred spustením ešte prispôsobiť uložte ju ako šablónu a pokračujte v úprave vyberte si jednu z možností nižšie a kliknite na tlačidlo uložiť kampaň nastavenia kampane môžete ľubovoľne'),
  ('SLOVENIAN', ' adsense stanje prijave za google adsense google adsense račun je bil začasno zamrznjen pozdravljeni hvala za vaše zanimanje v google adsense po pregledu vaše prijavnice so naši strokovnjaki ugotovili da spletna stran ki je trenutno povezana z vašim'),
  ('SPANISH', ' a continuación haz clic en el botón obtener ruta también puedes desplazarte hasta el final de la página para cambiar tus opciones de búsqueda gráfico y detalles ésta es una lista de los vídeos que te recomendamos nuestras recomendaciones se basan'),
  ('SWAHILI', ' a ujumbe mpya jumla unda tafuta na angalia vikundi vya kujadiliana na kushiriki mawazo iliyopangwa kwa tarehe watumiaji wapya futa orodha hizi lugha hoja vishikanisho vilivyo dhaminiwa ujumbe sanaa na tamasha toka udhibitisho wa neno kwa haraka fikia'),
  ('SWEDISH', ' a bort objekt från google desktop post äldst meny öretag dress etaljer alternativ för vad är inne yaste google skrivbord plugin program för nyheter google visa nyheter som är anpassade efter de artiklar som du läser om du till exempel läser'),
  ('TAGALOG', ' a na ugma sa google ay nakaka bantog sa gitna nang kliks na nangyayari sa pamamagitan nang ordinaryong paggagamit at sa kliks na likha nang pandaraya o hindi tunay na paggamit bunga nito nasasala namin ang mga kliks na hindi kailangan o hindi gusto nang'),
  ('TURKISH', ' a ayarlarınızı görmeniz ve yönetmeniz içindir eğer kampanyanız için günlük bütçenizi gözden geçirebileceğiniz yeri arıyorsanız kampanya yönetimi ne gidin kampanyanızı seçin ve kampanya ayarlarını düzenle yi tıklayın sunumu'),
  ('UKRAINIAN', ' а більший бюджет щоб забезпечити собі максимум прибутків від переходів відстежуйте свої об яви за датою географічним розташуванням'),
  ('URDU', ' آپ کو کم سے کم ممکنہ رقم چارج کرتا ہے اس کی مثال کے طور پر فرض کریں اگر آپ کی زیادہ سے زیادہ قیمت فی کلِک امریکی ڈالر اور کلِک کرنے کی شرح ہو تو'),
  ('VIETNAMESE', ' adsense cho nội dung nhà cung cấp dịch vụ di động xác minh tín dụng thay đổi nhãn kg các ô xem chi phí cho từ chối các đơn đặt hàng dạng cấp dữ liệu ác minh trang web của bạn để xem'),
  ('WELSH', ' a chofrestru eich cyfrif ymwelwch a unwaith i chi greu eich cyfrif mi fydd yn cael ei hysbysu o ch cyfeiriad ebost newydd fel eich bod yn gallu cadw mewn cysylltiad drwy gmail os nad ydych chi wedi clywed yn barod am gmail mae n gwasanaeth gwebost'),
  ('YIDDISH', 'און פאנטאזיע ער איז באקאנט צים מערסטן פאר זיינע באַלאַדעס ער האָט געוווינט אין ווארשע יעס פאריס ליווערפול און לאנדאן סוף כל סוף איז ער'),

  ('BOSNIAN', 'Novi predsjednik Mešihata Islamske zajednice u Srbiji (IZuS) i muftija dr. Mevlud ef. Dudić izjavio je u intervjuu za Anadolu Agency (AA) kako je uvjeren da će doći do vraćanja jedinstva među muslimanima i unutar Islamske zajednice na prostoru Sandžaka, te da je njegova ruka pružena za povratak svih u okrilje Islamske zajednice u Srbiji nakon skoro sedam godina podjela u tom dijelu Srbije. Dudić je za predsjednika Mešihata IZ u Srbiji izabran 4. januara, a zvanična inauguracija će biti obavljena u prvoj polovini februara. Kako se očekuje, prisustvovat će joj i reisu-l-ulema Islamske zajednice u Srbiji Husein ef. Kavazović koji će i zvanično promovirati Dudića u novog prvog čovjeka IZ u Srbiji. Dudić će danas boraviti u prvoj zvaničnoj posjeti reisu Kavazoviću, što je njegov privi simbolični potez nakon imenovanja. '),
  ('INDONESIAN', 'sukiyaki wikipedia indonesia ensiklopedia bebas berbahasa bebas berbahasa indonesia langsung ke navigasi cari untuk pengertian lain dari sukiyaki lihat sukiyaki irisan tipis daging sapi sayur sayuran dan tahu di dalam panci besi yang dimasak di atas meja makan dengan cara direbus sukiyaki dimakan dengan mence'),
  ('MALAY', 'sukiyaki wikipedia bahasa melayu ensiklopedia bebas sukiyaki dari wikipedia bahasa melayu ensiklopedia bebas lompat ke navigasi gelintar sukiyaki sukiyaki  hirisan tipis daging lembu sayur sayuran dan tauhu di dalam periuk besi yang dimasak di atas meja makan dengan cara rebusan sukiyaki dimakan dengan mence'),
  ('FRENCH', fr_en_Latn),

  # Added 2014.10.15
  ('KAZAKH',  'а билердің өзіне рұқсат берілмеген егер халық талап етсе ғана хан келісім берген өздеріңіз білесіздер қр қыл мыс тық кодексінде жазаның'),
  ('KURDISH',  'Nû pêvajo ya ezmûn ya pêşin di dîtin ku cezayên pêkan bi biryar standin, jûriyên neh zilam û sê jin wê gelektir govanan guhdar bike, bendewarî nav 3-mehan xilas be, ku zilamê Fransî yê 37 salê wê bi berdarî û heta mirinê bi avêtin zindanê.'),         # aka kmr
  ('KYRGYZ',  'агай эле оболу мен садыбакас аганын өзү менен эмес эмгектери менен тааныштым жылдары ташкенде өзбекстан илимдер академиясынын баяны'),
  ('MALAGASY',  'amporisihin i ianao mba hijery ny dika teksta ranofotsiny an ity lahatsoratra ity tsy ilaina ny opérateur efa karohina daholo ny teny rehetra nosoratanao ampiasao anaovana dokambarotra i google telugu datin ny takelaka fikarohana sary renitakelak i'),
  ('MALAYALAM',  'ം അങ്ങനെ ഞങ്ങള് അവരുടെ മുമ്പില് നിന്നു ഔടും ഉടനെ നിങ്ങള് പതിയിരിപ്പില് നിന്നു എഴുന്നേറ്റു'),
  ('BURMESE',  'တက္ကသုိလ္ မ္ဟ ပ္ရန္ လာ္ရပီးေနာက္ န္ဟစ္ အရ္ဝယ္ ဦးသန္ ့သည္ ပန္ းတနော္ အမ္ယုိးသား ေက္ယာင္ း'),
  ('NYANJA',  'Boma ndi gawo la dziko lomwe linapangidwa ndi cholinga chothandiza ntchito yolamulira. Kuŵalako kulikuunikabe mandita, Edipo nyima unalephera kugonjetsa kuŵalako.'),
  ('SINHALESE',  'අනුරාධ මිහිඳුකුල නමින් සකුරා ට ලිපියක් තැපෑලෙන් එවා තිබුණා කි ් රස්ටි ෂෙල්ටන් ප ් රනාන්දු ද'),     # aka SINHALA
  ('SESOTHO',  'bang ba nang le thahasello matshwao a sehlooho thuto e thehilweng hodima diphetho ke tsela ya ho ruta le ho ithuta e totobatsang hantle seo baithuti ba lokelang ho se fihlella ntlhatheo eo e sebetsang ka yona ke ya hore titjhere o hlakisa pele seo'),
  ('SUNDANESE',  'Nu ngatur kahirupan warga, keur kapentingan pamarentahan diatur ku RT, RW jeung Kepala Dusun, sedengkeun urusan adat dipupuhuan ku Kuncen jeung kepala adat. Sanajan Kampung Kuta teu pati anggang jeung lembur sejenna nu aya di wewengkon Desa Pasir Angin, tapi boh wangunan imah atawa tradisi kahirupan masarakatna nenggang ti nu lian.'),
  ('TAJIK',  'адолат ва инсондӯстиро бар фашизм нажодпарастӣ ва адоват тарҷеҳ додааст чоп кунед ба дигарон фиристед чоп кунед ба дигарон фиристед'),
  ('UZBEK',  'abadiylashtirildi aqsh ayol prezidentga tayyormi markaziy osiyo afg onistonga qanday yordam berishi mumkin ukrainada o zbekistonlik muhojirlar tazyiqdan shikoyat qilmoqda gruziya va ukraina hozircha natoga qabul qilinmaydi afg oniston o zbekistonni g'),
  ('UZBEK',  'а гапирадиган бўлсак бунинг иккита йўли бор биринчиси мана шу қуриган сатҳини қумликларни тўхтатиш учун экотизимни мустаҳкамлаш қумга'),

  # This is just the "version marker":
  ('TURKISH', 'qpdbmrmxyzptlkuuddlrlrbas las les qpdbmrmxyzptlkuuddlrlrbas el la qpdbmrmxyzptlkuuddlrlrbas'),
  )

fullTestData = tuple(x for x in testData[:-1] if x[0] != 'KURDISH') + (
  # Moved from small table to full table as of Oct 2014 release:
  ('SOMALI', ' a oo maanta bogga koobaad ugu qoran yahey beesha caalamka laakiin si kata oo beesha caalamku ula guntato soomaaliya waxa aan shaki ku jirin in aakhirataanka dadka soomaalida oo kaliya ay yihiin ku soomaaliya ka saari kara dhibka ay ku jirto'),
  ('IGBO', 'Chineke bụ aha ọzọ ndï omenala Igbo kpọro Chukwu. Mgbe ndị bekee bịara, ha mee ya nke ndi Christian. N\'echiche ndi ekpere chi Omenala Ndi Igbo, Christianity, Judaism, ma Islam, Chineke nwere ọtụtụ utu aha, ma nwee nanị otu aha. Ụzọ abụọ e si akpọ aha ahụ bụ Jehovah ma Ọ bụ Yahweh. Na ọtụtụ Akwụkwọ Nsọ, e wepụla aha Chineke ma jiri utu aha bụ Onyenwe Anyị ma ọ bụ Chineke dochie ya. Ma mgbe e dere akwụkwọ nsọ, aha ahụ bụ Jehova pụtara n’ime ya, ihe dị ka ugboro pụkụ asaa(7,000).'),
  ('HAUSA', ' a cikin a kan sakamako daga sakwannin a kan sakamako daga sakwannin daga ranar zuwa a kan sakamako daga guda daga ranar zuwa a kan sakamako daga shafukan daga ranar zuwa a kan sakamako daga guda a cikin last hour a kan sakamako daga guda daga kafar'),
  ('YORUBA', ' abinibi han ikawe alantakun le ni opolopo ede abinibi ti a to lesese bi eniyan to fe lo se fe lati se atunse jowo mo pe awon oju iwe itakunagbaye miran ti ako ni oniruru ede abinibi le faragba nipa atunse ninu se iwadi blogs ni ori itakun agbaye ti e ba'),
  ('ZULU', ' ana engu uma inkinga iqhubeka siza ubike kwi isexwayiso ngenxa yephutha lomlekeleli sikwazi ukubuyisela emuva kuphela imiphumela engaqediwe ukuthola imiphumela eqediwe zama ukulayisha kabusha leli khasi emizuzwini engu uma inkinga iqhubeka siza uthumele'),

  ('MONGOLIAN', 'ᠦᠭᠡ ᠵᠢᠨ ᠴᠢᠨᠭ᠎ᠠ ᠬᠦᠨᠳᠡᠢ ᠵᠢ ᠢᠯᠭᠠᠬᠣ'),
  ('X_Buginese', 'ᨄᨛᨑᨊᨒ ᨑᨗ ᨔᨒᨗᨓᨛ ᨕᨗᨋᨗᨔᨗ ᨒᨛᨄ ᨑᨛᨔᨛᨆᨗᨊ'),
  ('X_Gothic', '𐌰 𐌰𐌱𐍂𐌰𐌷𐌰𐌼 𐌰𐌲𐌲𐌹𐌻𐌹𐍃𐌺𐍃 𐌸𐌹𐌿𐌳𐌹𐍃𐌺𐍃 𐍆𐍂𐌰𐌲𐌺𐌹𐍃𐌺𐍃'),
  ('ABKHAZIAN', ' а зуа абзиара дақәшәоит ан лыбзиабара ахә амаӡам ауаҩы игәы иҭоу ихы иҿы ианубаалоит аҧҳәыс ҧшӡа ахацәа лышьҭоуп аҿаасҭа лара дрышьҭоуп'),
  ('AFAR', ' nagay tanito nagay tanto nagayna naharsi nahrur nake nala nammay nammay haytu nanu narig ne ni num numu o obare obe obe obisse oggole ogli olloyta ongorowe orbise othoga r rabe rade ra e rage rakub rasitte rasu reyta rog ruddi ruga s sa al bada sa ala'),
  ('AKAN', 'Wɔwoo Hilla Limann Mumu-Ɔpɛnimba 12 afe 1934. Wɔwoo no wɔ Gwollu wɔ Sisala Mantaw mu Nna ne maame yɛ Mma Hayawah. Ne papa so nna ɔyɛ Babini Yomu. Ɔwarr Fulera Limann ? Ne mba yɛ esuon-- Lariba Montia [wɔwoo no Limann]; Baba Limann; Sibi Andan [wɔwoo no Limann]; Lida Limann; Danni Limann; Zilla Limann na Salma Limann. Ɔtenaa ase kɔpemm Sanda-Kwakwa da ɛtɔ so 23 wɔ afe 1998 wɔ ?.'),
  ('AMHARIC', ' ለመጠይቅ ወደ እስክንድርያ ላኩዋቸውና የእስክንድርያ ጳጳስ አቴናስዮስ ፍሬምንጦስን እራሳቸውን ሾመው ልከዋል ከዚያ እስከ ዓ ም ድረስ የኢትዮጵያ አቡነ'),
  ('ASSAMESE', 'অঞ্চল নতুন সদস্যবৃন্দ সকলোৱে ভৰ্তি হব পাৰে মুল পৃষ্ঠা জন লেখক গুগ ল দল সাৰাংশ ই পত্ৰ টা বাৰ্তা এজন'),
  ('AYMARA', ' aru wijar aru ispañula ukaran aru witanam aru kurti aru kalis aru warani aru malta aru yatiyawi niya jakitanaka isluwiñ aru lmir phuran aru masirunan aru purtukal aru kruwat aru jakira urtu aru inklisa pirsan aru suyku aru malay aru jisk aptayma thaya'),
  ('BASHKIR', ' арналђан бындай ђилми эш тіркињлњ тњјге тапєыр нњшер ителњ ғинуар бєхет именлектє етешлектє ауыл ўќмерџєре хеџмєт юлын ћайлаѓанда'),
  ('BISLAMA', ' king wantaem nomo hem i sakem setan mo ol rabis enjel blong hem oli aot long heven oli kamdaon long wol taswe ol samting oli kam nogud olgeta long wol ya stat long revelesen ol faet kakae i sot ol sik mo fasin blong brekem loa oli kam antap olgeta samting'),
  ('BRETON', ' a chom met leuskel a ra e blas da jack irons dilabour hag aet kuit eus what is this dibab a reont da c houde michael beinhorn evit produiñ an trede pladenn kavet e vez ar ganaouennoù buhan ha buhan ganto setu stummet ar bladenn adkavet e vez enni funk'),
  ('BURMESE', ' တက္ကသုိလ္ မ္ဟ ပ္ရန္ လာ္ရပီးေနာက္ န္ဟစ္ အရ္ဝယ္ ဦးသန္ ့သည္ ပန္ းတနော္ အမ္ယုိးသား ေက္ယာင္ း'),
  ('CORSICAN', ' a prupusitu di risultati for utilizà a scatula per ricercà ind issi risultati servore errore u servore ha incuntratu una errore pruvisoria é ùn ha pussutu compie a vostra dumanda per piacè acimenta dinò ind una minuta tuttu listessu ligami truvà i'),
  ('DZONGKHA', ' རྩིས བརྐྱབ ཚུལ ལྡན དང ངེས བདེན སྦ སྟོན ནིའི དོན ལུ ཁྱོད གུག ཤད ལག ལེན འཐབ དགོ ག དང ཨིན པུཊི གྲལ ཐིག གུ'),
  ('ESPERANTO', ' a jarcento refoje per enmetado de koncerna pastro tiam de reformita konfesio ekde refoje ekzistis luteranaj komunumanoj tamen tiuj fondis propran komunumon nur en ambaŭ apartenis ekde al la evangela eklezio en prusio resp ties rejnlanda provinceklezio en'),
  ('FAROESE', ' at verða átaluverdar óhóskandi ella áloypandi vit kunnu ikki garanterða at google leitanin ikki finnur naka sum er áloypandi óhóskandi ella átaluvert og google tekur onga ábyrgd yvir tær síður sum koma við í okkara leitiskipan fá tær ein'),
  ('FIJIAN', ' i kina na i iri ka duatani na matana main a meke wesi se meke mada na meke ni yaqona oqo na meke ka dau vakayagataki ena yaqona vakaturaga e dau caka toka ga kina na vucu ka dau lagati tiko kina na ka e yaco tiko na talo ni wai ni yaqona na lewai ni wai'),
  ('FRISIAN', ' adfertinsjes gewoan lytse adfertinsjes mei besibbe siden dy t fan belang binne foar de ynhâld fan jo berjochten wolle jo mear witte fan gmail foardat jo jo oanmelde gean dan nei wy wurkje eltse dei om gmail te ferbetterjen dêrta sille wy jo sa út en'),
  ('GREENLANDIC', ' at nittartakkalli uani toqqarsimasatta akornanni nittartakkanut allanut ingerlaqqittoqarsinnaavoq kanukoka tassaavoq kommuneqarfiit kattuffiat nuna tamakkerlugu kommunit nittartagaannut ingerlaqqiffiusinnaasoq kisitsiserpassuit nunatsinnut tunngasut'),
  ('GUARANI', ' aháta añe ë ne mbo ehára ndive ajeruréta chupe oporandujey haĝua peëme mba épa pekaru ha áĝa oporandúvo nde eréta avei re paraguaýpe kachíke he i leúpe ndépa re úma kure tatakuápe ha leu ombohovái héë ha ujepéma kachíke he ijey'),
  ('HAWAIIAN', 'He puke noiʻi kūʻikena kūnoa ʻo Wikipikia. E ʻoluʻolu nō, e hāʻawi mai i kāu ʻike, kāu manaʻo, a me kou leo no ke kūkulu ʻana a me ke kākoʻo ʻana mai i ka Wikipikia Hawaiʻi. He kahua pūnaewele Hawaiʻi kēia no ka hoʻoulu ʻana i ka ʻike Hawaiʻi. Inā hiki iā ʻoe ke ʻōlelo Hawaiʻi, e ʻoluʻolu nō, e kōkua mai a e hoʻololi i nā ʻatikala ma ʻaneʻi, a pono e haʻi aku i kou mau hoa aloha e pili ana i ka Wikipikia Hawaiʻi. E ola mau nō ka ʻōlelo Hawaiʻi a mau loa aku.'),
  ('IGBO', 'Chineke bụ aha ọzọ ndï omenala Igbo kpọro Chukwu. Mgbe ndị bekee bịara, ha mee ya nke ndi Christian. N\'echiche ndi ekpere chi Omenala Ndi Igbo, Christianity, Judaism, ma Islam, Chineke nwere ọtụtụ utu aha, ma nwee nanị otu aha. Ụzọ abụọ e si akpọ aha ahụ bụ Jehovah ma Ọ bụ Yahweh. Na ọtụtụ Akwụkwọ Nsọ, e wepụla aha Chineke ma jiri utu aha bụ Onyenwe Anyị ma ọ bụ Chineke dochie ya. Ma mgbe e dere akwụkwọ nsọ, aha ahụ bụ Jehova pụtara n’ime ya, ihe dị ka ugboro pụkụ asaa(7,000).'),
  ('INTERLINGUA', ' super le sitos que tu visita isto es necessari pro render disponibile alcun functionalitates del barra de utensiles a fin que nos pote monstrar informationes ulterior super un sito le barra de utensiles debe dicer a nos le'),
  ('INTERLINGUE', ' abhorre exceptiones in li derivation plu cardinal por un l i es li regularità del flexion conjugation ples comparar latino sine flexione e li antiqui projectes naturalistic queles have quasi null regules de derivation ma si on nu examina li enunciationes'),
  ('INUPIAK', 'sabvaqjuktuq sabvaba atiqaqpa atiqaqpa ibiq iebiq ixafich niuqtulgiññatif uvani natural gas tatpikka ufasiksigiruaq maaffa savaannafarufa mi tatkivani navy qanuqjugugguuq taaptuma inna uqsrunik ivaqjiqhutik       taktuk allualiuqtuq sigukun nanuq puuvraatuq taktuum amugaa kalumnitigun nanuq agliruq allualiuqtuq'),
  ('KASHMIRI', ' ژماں سرابن منز  گرٲن چھِہ خابٕک کھلونہٕ ؤڈراواں   تُلتِھ نِیَس تہٕ گوشہِ گوشہِ مندچھاوى۪س   دِلس چھُہ وون٘ت وُچھان از ستم قلم  صبوٝرٕ وول مسٲفر لیۆکھُن بێتابن منز   ورل سوال چھُہ تراواں جوابن منز    کالہٕ پھۯستہٕ پھن٘ب پگَہہ پہ   پۆت نظر دِژ نہٕ ژھالہٕ مٔت آرن     مٲنز مسول متھان چھےٚ مس والن  وۅن چھےٚ غارن تہِ نارٕ ژھٹھ ژاپان  رێش تۅرگ تراوٕہن تہٕ ون رٹہٕ ہن  ہوشہِ ہێۆچھ نہٕ پوشنوٝلس نِش  مۅہرٕ دی دی زٕلاں چھِ زى۪و حرفن  لۆدرٕ پھٔل ہى۪تھ ملر عازمؔ  سۆدرٕ کھۅنہِ منز منگاں چھُہ ندرى۪ن پن   ژے تھى۪کی یہِ مسٲفر پنن وُڈو تہٕ پڑاو   گٕتَو گٕتَو چھےٚ یہِ کۅل بُتھ تہٕ بانہٕ سٕہہ گۅردٕ چھہِ سپداں دمہٕ پُھٹ  چھِٹہ پونپر پکھہٕ داران سُہ یتى۪ن تۯاوِ  کم نظر دۯاکھ تہٕ باسیوے سُہ مۆہ ہیو یێران  مےٚ ژى۪تُرمُت چھُہ سُلی تس چھےٚ کتى۪ن تھپھ  شاد مس کراں وُچھ مےٚ خون  ژٕ خبر کیازِ کراں دۯاکھ تمِس پى۪ٹھ ماتم  أز کہِ شبہٕ آو مےٚ بێیہِ پیش سفر زانہِ خدا  دارِ پى۪ٹھ ژٲنگ ہنا تھو زِ ژے چھےٚ مێون  أنہٕ کپٹاں چھُہ زٕژن سون مظفّر عازمؔ  پوشہ برگن چھُہ سُواں چاکھ سُہ الماس قلم   لوِ کٔ ڈ نوِ سرٕ سونتس کل   پروِ بۆر بێیہ از بانبرِ ہۆت  یمبرزلہِ ٹارى۪ن منز نار   وزملہِ کۅسہٕ کتھ کٔر اظہار  کچھہِ منزٕ ؤن رووُم اچھہِ  چشمو ژوپُم کٔنڈ انبار   تماشہِ چھہِ تگاں'),
  ('KAZAKH', ' ﺎ ﻗﻴﺎﻧﺎﺕ ﺑﻮﻟﻤﺎﻳﺪﻯ ﺑﯘﻝ ﭘﺮﻭﺗﺴﻪﺳﯩﻦ ﻳﺎﻋﻨﻲ ﻗﺎﻻ ﻭﻣﯩﺮﯨﻨﺪﻩ ﻗﺎﺯﺍﻕ ء ﺗﯩﻠﯩﻨﯩﯔ ﻗﻮﻟﺪﺍﻧﯩﻠﻤﺎﯞﻯ ﻗﺎﺯﺍﻕ ﺟﻪﺭﯨﻨﺪﻩ'),
  ('KAZAKH', ' а билердің өзіне рұқсат берілмеген егер халық талап етсе ғана хан келісім берген өздеріңіз білесіздер қр қыл мыс тық кодексінде жазаның'),
  ('KHASI', ' kaba jem jai sa sngap thuh ia ki bynta ba sharum naka sohbuin jong phi nangta sa pynhiar ia ka kti kadiang jong phi sha ka krung jong phi bad da kaba pyndonkam kumjuh ia ki shympriahti jong phi sa sngap thuh shapoh ka tohtit jong phi pyndonkam ia kajuh ka'),
  ('KURDISH', ' بۆ به ڕێوه بردنی نامه ی که دێتن ڕاسته وخۆ ڕه وان بکه نامه کانی گ مایل بۆ حسابی پۆستێکی تر هێنانی په یوه ندکاره کان له'),
  ('KYRGYZ', ' جانا انى تانۇۇ ۇلۇتۇن تانۇۇ قىرعىزدى بئلۉۉ دەگەندىك اچىق ايتساق ماناستى تاانىعاندىق ۅزۉڭدۉ تاانىعاندىق بۉگۉن تەما جۉكتۅمۅ ق ى رع ى ز ت ى ل ى'),
  ('KYRGYZ', ' агай эле оболу мен садыбакас аганын өзү менен эмес эмгектери менен тааныштым жылдары ташкенде өзбекстан илимдер академиясынын баяны'),
  ('LATIN', ' a deo qui enim nocendi causa mentiri solet si iam consulendi causa mentiatur multum profecit sed aliud est quod per se ipsum laudabile proponitur aliud quod in deterioris comparatione praeponitur aliter enim gratulamur cum sanus est homo aliter cum melius'),
  ('LINGALA', ' abakisamaki ndenge esengeli moyebami abongisamaki solo mpenza kombo ya moyebami elonguamaki kombo ya bayebami elonguamaki kombo eleki molayi po na esika epesameli limbisa esika ya kotia ba kombo esuki boye esengeli olimbola ndako na yo ya mikanda kombo'),
  ('LUXEMBOURGISH', ' a gewerkschaften och hei gefuerdert dir dammen an dir häre vun de gewerkschaften denkt un déi aarm wann der äer fuerderunge formuléiert d sechst congés woch an aarbechtszäitverkierzung hëllefen hinnen net d unhiewe vun de steigerungssäz bei de'),
  ('MALAGASY', ' amporisihin i ianao mba hijery ny dika teksta ranofotsiny an ity lahatsoratra ity tsy ilaina ny opérateur efa karohina daholo ny teny rehetra nosoratanao ampiasao anaovana dokambarotra i google telugu datin ny takelaka fikarohana sary renitakelak i'),
  ('MALAY', 'bilik sebelah berkata julai pada pm ladymariah hmm sume ni terpulang kepada individu mungkin anda bernasib baik selama ini dalam membeli hp yang bagus deli berkata julai pada pm walaupun bukan bahsa baku tp tetap bahasa melayu kan perubahan boleh dibuat'),
  ('MANX', ' and not ripe as i thought yn assyl yn shynnagh as yn lion the ass the fox and the lion va assyl as shynnagh ayns commee son nyn vendeilys as sauchys hie ad magh ayns y cheyll dy shelg cha row ad er gholl feer foddey tra veeit ad rish lion yn shynnagh'),
  ('MAORI', ' haere ki te kainga o o haere ki te kainga o o haere ki te kainga o te rapunga ahua o haere ki te kainga o ka tangohia he ki to rapunga kaore au mohio te tikanga whakatiki o te ra he whakaharuru te pai rapunga a te rapunga ahua a e kainga o nga awhina o te'),
  ('MAURITIAN_CREOLE', 'Anz dir mwa, Sa bann delo ki to trouve la, kot fam prostitie asize, samem bann pep, bann lafoul dimoun, bann nasion ek bann langaz. Sa dis korn ki to finn trouve, ansam avek bebet la, zot pou ena laenn pou prostitie la; zot pou pran tou seki li ena e met li touni, zot pou manz so laser e bril seki reste dan dife. Parski Bondie finn met dan zot leker proze pou realiz so plan. Zot pou met zot dakor pou sed zot pouvwar bebet la ziska ki parol Bondie fini realize.'),
  ('MONGOLIAN', ' а боловсронгуй болгох орон нутгийн ажил үйлсийг уялдуулж зохицуулах дүрэм журам боловсруулах орон нутгийн өмч хөрөнгө санхүүгийн'),
  ('NAURU', ' arcol obabakaen riringa itorere ibibokiei ababaro min kuduwa airumena baoin tokin rowiowet itiket keram damadamit eigirow etoreiy row keitsito boney ibingo itsiw dorerin naoerodelaporte s nauruan dictionary a c a c d g h o p s t y aiquen ion eins aiquen'),
  ('NDEBELE', "ikomiti elawulako yegatja  emhlanganweni walo ]imithetho mgomo ye anc ibekwa malunga wayo begodu ubudosiphambili kugandelela lokho okutjhiwo yi  lokha nayithi abantu ngibo  "),
  ('NORWEGIAN_N', ' a for verktylina til å hjelpa deg å nå oss merk at pagerank syninga ikkje automatisk kjem til å henta inn informasjon frå sider med argument dvs frå sider med eit i en dersom datamaskina di er plassert bak ein mellomtenar for vevsider kan det verka'),
  ('NYANJA', 'Boma ndi gawo la dziko lomwe linapangidwa ndi cholinga chothandiza ntchito yolamulira. Kuŵalako kulikuunikabe mandita, Edipo nyima unalephera kugonjetsa kuŵalako.'),
  ('OCCITAN', '  Pasmens, la classificacion pus admesa uei (segon Juli Ronjat e Pèire Bèc) agropa lei parlars deis Aups dins l\'occitan vivaroaupenc e non dins lo dialècte provençau.'),
  ('OROMO', ' afaan katalaa bork bork bork hiikaa jira hin argamne gareen barbaadame hin argamne gargarsa qube en gar bayee jira garee walitti firooman gareewwan walitti firooman fuula web akka tartiiba qubeetiin agarsiisi akka tartiiba qubeetiin agarsiisaa jira akka'),
  ('PASHTO', ' اتو مستقل رياست جوړ شو او د پخواني ادبي انجمن څانګې ددې رياست جز شوی او ددې انجمن د ژبې مديريت د پښتو ټولنې په لوی مديريت واوښت لوی مدير يې د'),
  ('PEDI', 'Bophara bja Asia ekaba 8.6% bja lefase goba 29.4% bja naga ya lefase (ntle le mawatle). Asia enale badudu bao bakabago dimillione millione tše nne (4 billion) yeo e bago 60% ya badudi ba lefase ka bophara. A bapolelwa rena sefapanong mehleng ya Pontius Pilatus. A hlokofatšwa, A bolokwa, A tsoga ka letšatši la boraro, ka mo mangwalo a bolelago ka gona, a rotogela magodimong, '),
  ('QUECHUA', ' is t ipanakunatapis rikuchinankupaq qanpa simiykipi noqaykoqpa uya jllanakunamanta kunan jamoq simikunaman qelqan tiyan watukuy qpa uyata qanpa llaqtaykipi llank anakuna simimanta yanapakuna simimanta mayqen llaqtallapis kay simimanta t ijray qpa qelqa'),
  ('RHAETO_ROMANCE', ' Cur ch’il chantun Turitg ha dà il dretg da votar a las dunnas (1970) è ella vegnida elegida en il cussegl da vischnanca da Zumikon per la Partida liberaldemocratica svizra (PLD). Da 1974 enfin 1982 è ella stada presidenta da vischnanca da Zumikon. L’onn 1979 è Elisabeth Kopp vegnida elegida en il Cussegl naziunal e reelegida quatter onns pli tard cun in resultat da sur 100 000 vuschs. L’onn 1984 è ella daventada vicepresidenta da la PLD.'),
  ('RUNDI', ' ishaka mu ndero y abana bawe ganira n abigisha nimba hari ingorane izo ari zo zose ushobora gusaba kubonana n umwigisha canke kuvugana nawe kuri terefone inyuma y uko babarungikira urutonde rw amanota i muhira mu bisanzwe amashure aratumira abavyeyi'),
  ('SAMOAN', ' autu mea o lo totonu le e le minaomia matou te tuu i totonu i le faamatalaina o le suesuega i taimi uma mea o lo totonu fuafua i mea e tatau fa afoi tala mai le newsgroup mataupu fa afoi mai tala e ai le mataupu e ai totonu tusitala o le itu o faamatalaga'),
  ('SANGO', ' atâa na âkotta zo me lâkwê angbâ gï tarrango nî âkotta zo tî koddoro nî âde agbû tenne nî na kate töngana mbênî kotta kpalle tî nzönî dutï tî halëzo pëpe atâa sô âla lü gbâ tî ândya tî mâi na sahngo asâra gbâ tî'),
  ('SANSKRIT', ' ं क र्मणस् त स्य य त्कि ङ्चेह करो त्यय ं त स्माल् लोका त्पु नरै ति अस्मै लोका य क र्मण इ ति नु काम'),
  ('SANSKRIT', ' brahmā tatraivāntaradhīyata tataḥ saśiṣyo vālmīkir munir vismayam āyayau tasya śiṣyās tataḥ sarve jaguḥ ślokam imaṃ punaḥ muhur muhuḥ prīyamāṇāḥ prāhuś ca bhṛśavismitāḥ samākṣaraiś caturbhir yaḥ pādair gīto'),
  ('SCOTS', ' a gless an geordie runciman ower a gless an tamson their man preached a hale hoor aboot the glorious memories o forty three an backsliders an profane persons like esau an aboot jeroboam the son o nebat that gaed stravagin to anither kirk an made aa israel'),
  ('SESELWA', 'Sesel ou menm nou sel patri. Kot nou viv dan larmoni. Lazwa, lanmour ek lape. Nou remersye Bondye. Preserv labote nou pei. Larises nou losean. En leritaz byen presye. Pour boner nou zanfan. Reste touzour dan linite. Fer monte nou paviyon. Ansanm pou tou leternite. Koste Seselwa!'),
  ('SESOTHO', ' bang ba nang le thahasello matshwao a sehlooho thuto e thehilweng hodima diphetho ke tsela ya ho ruta le ho ithuta e totobatsang hantle seo baithuti ba lokelang ho se fihlella ntlhatheo eo e sebetsang ka yona ke ya hore titjhere o hlakisa pele seo'),
  ('SHONA', ' chete vanyori vanotevera vakabatsira kunyora zvikamu zvino kumba home tinyorere tsamba chikamu chakumbirwa hachina kuwanikwa chikamu ichi cheninge chakayiswa kuimwe nzvimbo mudhairekitori rino chimwe chikamu chopadhuze pane chinhu chatadza kushanda bad'),
  ('SINDHI', ' اضافو ٿي ٿيو پر اها خبر عثمان کي بعد پيئي ته سگريٽ ڇڪيندڙ مسلمان نه هو بلڪ هندو هو دڪان تي پهچي عثمان ڪسبت کولي گراهڪن جي سيرب لاهڻ شروع ڪئي پر'),
  ('SISWANT', ' bakhokhintsela yesikhashana bafake imininingwane ye akhawunti leliciniso kulelifomu nangabe akukafakwa imininingwane leliciniso imali lekhokhiwe angeke ifakwe kumkhokhintsela lofanele imininingwane ye akhawunti ime ngalendlela lelandzelako inombolo'),
  ('SUNDANESE', 'Nu ngatur kahirupan warga, keur kapentingan pamarentahan diatur ku RT, RW jeung Kepala Dusun, sedengkeun urusan adat dipupuhuan ku Kuncen jeung kepala adat. Sanajan Kampung Kuta teu pati anggang jeung lembur sejenna nu aya di wewengkon Desa Pasir Angin, tapi boh wangunan imah atawa tradisi kahirupan masarakatna nenggang ti nu lian.'),
  ('TAJIK', ' адолат ва инсондӯстиро бар фашизм нажодпарастӣ ва адоват тарҷеҳ додааст чоп кунед ба дигарон фиристед чоп кунед ба дигарон фиристед'),
  ('TATAR', 'ачарга да бирмәде чәт чәт килеп тора безнең абыйнымы олы абыйнымы эштән'),
  ('TATAR', ' alarnı eşkärtü proğramnarın eşläwen däwam itü tatar söylämen buldıru wä sizep alu sistemnarın eşläwen däwat itü häm başqalar yılnıñ mayında tatar internetı ictimağıy oyışması milli ts isemle berençe däräcäle häm tat'),
  ('TIBETAN', ' ་གྱིས་ཁ་ཆེའི་ཕྱག་འཚལ་ཁང་ཞིག་བཤིག་སྲིད་པ། ཡར་ཀླུང་གཙང་པོར་ཆ ུ་མཛོང་བརྒྱག་རྒྱུའི་ལས་འཆར་ལ་རྒྱ་གར་གྱི་སེམས་ཚབས། རྒྱ་གརགྱི་མཚོ་འོག་དམག་གྲུར་སྦར་གས་བྱུང་བ། པ་ཀི་སི་ཏན་གྱིས་རྒྱ་གར་ལ་མི་སེར་བསད་པའི་སྐྱོན་འཛུགས་བྱས་པ། རྩོམ་ཡིག་མང་བ། འབྲེལ་མཐུད་བརྒྱུད་ལམ། ཐོན་སྐྱེད་དང་སྲི་ཞུ། ་ཐོག་དེབ་བཞི་ དཔར་འགྲེམས་གནང་ཡོད་པ་དང་བོད་ཡིག་དྲ་ཚིགས་ཁག་ནང་ལ་ཡང་རྩོམ་ཡང་ཡང་བྲིས་གནང་མཁན་རེད། ལེ་ཚན་ཁག ལེ་ཚན་ཁག འབྲེལ་ཡོད། འགྲེམ་སྟོན། རྒྱུད་ལམ་སྣ་མང་ཡིག་མཛོད། བཀོལ་སྤྱོད་པའི་འཇོག་ཡུལ་དྲ་ངོས། སྔོན་མ། རྗེས་མ། བསྟན་འཛིན་བདེ་སྐྱིད། ཚེ་རིང་རྣམ་རྒྱལ། བསྟན་འཛིན་ངག་དབང་། ཡོལ་གདོང་ཚེ་རིང་ལྷག་པ།  ་དབང་ ཕྱུག་གཉིས་ཀྱིས་བརྗོད་གཞི་བྱེ་བྲག་པ་ཞིག་ལ་བགྲོ་གླེང་གཏིང་ཟབ་བྱེད་པའི་གཟའ་ འཁོར་གཉིས་རེའི་མཚམས་ཀྱི་ལེ་ཚན་ཞིག་ཡིན། དཔྱད་ཞིབ་ཀྱིས་རྒྱ་ནག་ནང་ཁུལ་གྱི་འགྱུར་ལྡོག་དང༌། རྒྱ་ནག་དང་རྒྱལ་སྤྱིའི་འབྲེལ་བར་དམིགས་སུ་བཀར་ནས་བགྲོ་གླེང་བྱེད་ཀྱི་ཡོད།། རྒྱང་སྲིང་དུས་ཚོད།'),
  ('TIGRINYA', ' ሃገር ተረፎም ዘለዉ ኢትዮጵያውያን ኣብቲ ምስ ኢትዮጵያ ዝዳውብ ኣውራጃ ደቡብ ንኽነብሩ ኣይፍቀደሎምን እዩ ካብ ሃገር ንኽትወጽእ ዜጋ ኹን ወጻእተኛ ናይ'),
  ('TONGA', ' a ke kumi oku ikai ke ma u vakai ki hono hokohoko faka alafapeti api pe ko e uluaki peesi a ho o fekumi faka malatihi fekumi ki he lea oku fakaha atu pe ko ha fonua fekumi ki he fekumi ki he peesi oku ngaahi me a oku sai imisi alu ki he ki he ulu aki'),
  ('TSONGA', ' a ku na timhaka leti nga ta vulavuriwa na google google yi hlonipha yi tlhela yi sirheleta vanhu hinkwavo lava tirhisaka google toolbar ku dyondza hi vusireleli eka system ya hina hi kombela u hlaya vusireleli bya hina eka toolbar mbulavulo wu tshikiwile'),
  ('TSWANA', ' go etela batla ditsebe tsa web tse di nang le le batla ditsebe tse di golaganya le tswang mo leka go batla web yotlhe batla mo web yotlhe go bona home page ya google batla mo a o ne o batla gore a o ne o batla ditsebe tsa bihari batla mo re maswabi ga go'),
  ('TURKMEN', ' айдянларына ынанярмыка эхли боз мейданлары сурулип гутарылан тебигы ота гарып гумлукларда миллиондан да артыкмач ири шахлы малы миллиона'),
  ('TURKMEN', ' akyllylyk çyn söýgi üçin böwet däl de tebigylykdyr duýgularyň gödeňsiligi aç açanlygy bahyllygy söýgini betnyşanlyk derejesine düşürýändir söýeni söý söýmedige süýkenme özüni söýmeýändigini görmek ýigit üçin uly'),
  ('AKAN', ' amammui tumidifo no bɛtow ahyɛ atoro som so mpofirim na wɔasɛe no pasaa ma ayɛ nwonwa dɛn na ɛbɛka wɔn ma wɔayɛ saa bible no ma ho mmuae wɔ adiyisɛm nhoma no mu sɛ onyankopɔn na ɔde hyɛɛ wɔn komam sɛ wɔmma ne nsusuwii mmra mu'),
  ('UIGHUR', ' ئالەملەرنىڭ پەرۋەردىگارىدىن تىلەيمەن سىلەر بۇ يەرلەردە باغچىلاردىن بۇلاقلاردىن زىرائەتلەردىن يۇمشاق پىشقان خورمىلاردىن بەھرىمەن بولۇپ'),
  ('UIGHUR', ' а башлиди әмма бу қетимқи канада мәтбуатлириниң хәвәрлиридә илгирикидәк хитай һөкүмәт мәтбуатлиридин нәқил алидиған вә уни көчүрүп'),
  ('UZBEK', ' آرقلی بوتون سیاسی حزب و گروه لرفعالیتیگه رخصت بیرگن اخبارات واسطه لری شو ییل مدتیده مثال سیز ترقی تاپکن و اهالی نینگ اقتصادی وضعیتی اوتمیش'),
  ('UZBEK', ' а гапирадиган бўлсак бунинг иккита йўли бор биринчиси мана шу қуриган сатҳини қумликларни тўхтатиш учун экотизимни мустаҳкамлаш қумга'),
  ('UZBEK', ' abadiylashtirildi aqsh ayol prezidentga tayyormi markaziy osiyo afg onistonga qanday yordam berishi mumkin ukrainada o zbekistonlik muhojirlar tazyiqdan shikoyat qilmoqda gruziya va ukraina hozircha natoga qabul qilinmaydi afg oniston o zbekistonni g'),
  ('VENDA', 'Vho ṱanganedzwa kha Wikipedia nga tshiVenḓa. Vhadivhi vha manwalo a TshiVenda vha talusa divhazwakale na vhubvo ha Vhavenda ngau fhambana. Vha tikedza mbuno dzavho uya nga mawanwa a thoduluso dze vha ita. Vhanwe vha vhatodulusi vhari Vhavenda vho tumbuka Afrika vhukati vha tshimbila vha tshiya Tshipembe ha Afrika, Rhodesia hune ha vho vhidzwa Zimbagwe namusi.'),
  ('VOLAPUK', ' brefik se volapükavol nüm balid äpubon ün dü lif lölik okas redakans älaipübons gasedi at nomöfiko äd ai mu kuratiko pläo timü koup nedäna fa ns deutän kü päproibon fa koupanef me gased at ästeifülom ad propagidön volapüki as sam ün'),
  ('WARAY_PHILIPPINES', 'Amo ini an balay han Winaray o Binisaya nga Lineyte-Samarnon nga Wikipedia, an libre ngan gawasnon nga ensayklopedya nga bisan hin-o puyde magliwat o mag-edit. An Wikipedia syahan gintikang ha Iningles nga yinaknan han tuig 2001. Ini nga bersyon Winaray gintikang han ika-25 han Septyembre 2005 ngan ha yana mayda 514,613 nga artikulo. Kon karuyag niyo magsari o magprobar, pakadto ha . An Gastrotheca pulchra[2] in uska species han Anura nga ginhulagway ni Ulisses Caramaschi ngan Rodrigues hadton 2007. An Gastrotheca pulchra in nahilalakip ha genus nga Gastrotheca, ngan familia nga Hemiphractidae.[3][4] Ginklasipika han IUCN an species komo kulang hin datos.[1] Waray hini subspecies nga nakalista.[3]'),
  ('WOLOF', ' am ak dëgg dëggam ak gëm aji bind ji te gëstu ko te jëfandikoo tegtalu xel ci saxal ko sokraat nag jëfandikoo woon na xeltu ngir tas jikko yu rafet ci biir nit ñi ak dëggu ak soppante sokraat nag ñëw na mook aflaton platon sukkandiku ci ñaari'),
  ('XHOSA', ' a naynga zonke futhi libhengezwa kwiwebsite yebond yasemzantsi afrika izinga elisebenzayo xa usenza olu tyalo mali liya kusebenza de liphele ixesha lotyalo mali lwakho inzala ihlawulwa rhoqo emva kweenyanga ezintandathu ngomhla wamashumi amathathu ananye'),
  ('X_KLINGON', ' a ghuv bid soh naq jih lodni yisov chich wo vamvo qeylis lunge pu chah povpu vodleh a dah ghah cho ej dah wo che pujwi bommu tlhegh darinmohlahchu pu majqa horey so lom qa ip quv law may vad suvtahbogh wa sanid utlh quv pus datu pu a vitu chu pu johwi tar'),
  ('X_PIG_LATIN', ' away ackupbay editcray ardcay ybay isitingvay ouryay illingbay eferencespray agepay orway isitvay ethay adwordsway elphay entrecay orfay oremay etailsday adwordsway ooglegay omcay upportsay'),
  ('ZHUANG', ' dih yinzminz ndaej daengz bujbienq youjyau dih cingzyin caeuq cinhingz diuz daihit boux boux ma daengz lajmbwn couh miz cwyouz cinhyenz caeuq genzli bouxboux bingzdaengj gyoengq vunz miz lijsing caeuq liengzsim wngdang daih gyoengq de lumj beixnuengx'),

  # This is just the "version marker":
  ('ICELANDIC', 'qpdbmrmxyzptlkuuddlrlrbas las les qpdbmrmxyzptlkuuddlrlrbas el la qpdbmrmxyzptlkuuddlrlrbas'),
)

# Simple English with bad UTF-8
TEST_EN_LATN_BAD_UTF8 = b'Forty good bytes followed by bad UTF-8:\'\xC0\xA9\' and then good again.';

class TestCLD(unittest.TestCase):

  langsSeen = set()
  fullLangsSeen = set()

  def runOne(self, expectedLangName, s, doFull = False):
    if VERBOSE:
      print('')
      print('Test: %s [%d bytes]' % (expectedLangName, len(s)))
    failed = False
    for isPlainText in False, True:
      if doFull:
        detector = cld2full.detect
      else:
        detector = cld2.detect
      isReliable, textBytesFound, details = detector(s, isPlainText=isPlainText)
      if len(details) > 0:
        detectedLangName, detectedLangeCode = details[0][:2]

        if VERBOSE:
          print('  detected: %s' % detectedLangName)
          print('  reliable: %s' % (isReliable != 0))
          print('  textBytes: %s' % textBytesFound)
          print('  details: %s' % str(details))

        try:
          self.assertEqual(expectedLangName, detectedLangName, 'full?=%s %s != %s; details: %s' % (doFull, detectedLangName, expectedLangName, str(details)))
        except:
          traceback.print_exc()
          failed = True
          break
        if doFull:
          self.fullLangsSeen.add(detectedLangName)
        else:
          self.langsSeen.add(detectedLangName)
      else:
        try:
          self.fail('no language detected; expected %s' % expectedLangName)
        except:
          traceback.print_exc()
          failed = True
          break

    if failed:
      self.fail('some languages were wrong')

  def test_basic(self):
    for lang, text in testData:
      self.runOne(lang, text)
    for lang, text in fullTestData:
      self.runOne(lang, text, True)

  # End of per-language tests; start tests for specific functions:
  def test_vectors(self):
    for detector in cld2, cld2full:
      for lang, text in testData:
        isReliable, textBytesFound, details, vectors = detector.detect(text, returnVectors=True)
        self.assertTrue(textBytesFound > 0)
        if text == fr_en_Latn:
          self.assertEqual(3, len(vectors))
          self.assertEqual(('en', 'fr', 'en'), tuple(x[3] for x in vectors))

  def test_encoding_hint(self):
    for detector in cld2, cld2full:
      for lang, text in testData:
        for encoding in cld2.ENCODINGS:
          detector.detect(text, hintEncoding=encoding)

  def test_language_hint(self):
    for detector in cld2, cld2full:
      for lang, text in testData:
        for langHint in cld2.LANGUAGES:
          detector.detect(text, hintLanguage=langHint[0])
          detector.detect(text, hintLanguage=langHint[1])

  def test_top_level_domain_hint(self):
    for detector in cld2, cld2full:
      for lang, text in testData:
        detector.detect(text, hintTopLevelDomain='edu')
        detector.detect(text, hintTopLevelDomain='com')
        detector.detect(text, hintTopLevelDomain='id')

  def test_language_http_headers_hint(self):
    for detector in cld2, cld2full:
      for lang, text in testData:
        detector.detect(text, hintLanguageHTTPHeaders='mi,en')

  def test_debug_flags(self):
    for detector in cld2, cld2full:
      detector.detect(fr_en_Latn, debugScoreAsQuads=True)
      detector.detect(fr_en_Latn, debugHTML=True)
      detector.detect(fr_en_Latn, debugHTML=True, debugCR=True)
      detector.detect(fr_en_Latn, debugHTML=True, debugQuiet=True)
      detector.detect(fr_en_Latn, debugHTML=True, debugVerbose=True)
      detector.detect(fr_en_Latn, debugHTML=True, debugEcho=True)

  def test_unreliable(self):
    for detector in cld2, cld2full:
      isReliable, textBytesFound, details, vectors = detector.detect('interaktive infografik \xc3\xbcber videospielkonsolen', returnVectors = True)
      self.assertEqual(3, len(details))

  def test_random_bytes(self):
    for detector in cld2, cld2full:
      for i in range(100):
        # This hits SEGV in versions before 20141016:
        try:
          isReliable, textBytesFound, details, vectors = detector.detect(os.urandom(100), returnVectors = True)
        except ValueError:
          # expected
          pass

  def test_invalid_utf8(self):
    for detector in cld2, cld2full:
      try:
        isReliable, textBytesFound, details, vectors = detector.detect(TEST_EN_LATN_BAD_UTF8, returnVectors = True)
        self.fail('did not hit expected exception: %s vs %s' % (textBytesFound, len(TEST_EN_LATN_BAD_UTF8)))
      except ValueError:
        # expected
        pass
      except:
        print('GOT WRONG EXC: %s vs %s: %s' % (str(sys.exc_info()), cld2.error, cld2.error == sys.exc_info()[0]))

  def test_best_effort(self):
    for detector in cld2, cld2full:
      isReliable, textBytesFound, details = detector.detect('interaktive infografik \xc3\xbcber videospielkonsolen')

      # Too little text:
      self.assertFalse(isReliable)
      self.assertEqual(details[0][0], 'Unknown')

      # Do it again, forcing bestEffort:
      isReliable, textBytesFound, details = detector.detect('interaktive infografik \xc3\xbcber videospielkonsolen', bestEffort=True)
      self.assertTrue(isReliable)
      self.assertNotEqual(details[0][0], 'Unknown')

if __name__ == '__main__':
  try:
    unittest.main()
  finally:

    # Confirm that cld2.DETECTED_LANGUAGES == all languages detected by
    # the test cases:
    for lang in cld2.DETECTED_LANGUAGES:
      # Raises KeyError if lang was never detected by the test:
      TestCLD.langsSeen.remove(lang)
    # Confirm that no languages detected by the test were not listed in cld2.DETECTED_LANGUAGES:
    if len(TestCLD.langsSeen) != 0:
      raise RuntimeError('unexpected additional languages were detected: %s' % TestCLD.langsSeen)

    if False:
      l = list(TestCLD.fullLangsSeen)
      l.sort()
      for x in l:
        print('PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("%s"));' % x)

    # Confirm that cld2full.DETECTED_LANGUAGES == all languages detected by
    # the test cases:

    #print('FULL %d: %s' % (len(TestCLD.fullLangsSeen), ', '.join(TestCLD.fullLangsSeen)))
    for lang in cld2full.DETECTED_LANGUAGES:
      # Raises KeyError if lang was never detected by the test:
      TestCLD.fullLangsSeen.remove(lang)
    # Confirm that no languages detected by the test were not listed in cld2full.DETECTED_LANGUAGES:
    if len(TestCLD.fullLangsSeen) != 0:
      raise RuntimeError('unexpected additional languages were detected: %s' % TestCLD.fullLangsSeen)
