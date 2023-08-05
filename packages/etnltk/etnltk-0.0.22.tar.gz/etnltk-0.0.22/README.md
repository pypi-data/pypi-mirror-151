# Ethiopian Natural Language Toolkit (etnltk)

- The Ethiopian Natural Language Toolkit (etnltk) project aimed to develop a suite of open source Natural Language Processing modules for the Ethiopian languages.
- The Ethiopian Natural Language Toolkit (etnltk) is built using python language and takes inspiration from `spacy` and `nltk` libraries.

## Installation

### pip

- **etnltk** supports Python 3.6 or later. We recommend that you install etnltk via `pip`, the Python package manager. To install, simply run:

  ```python
    pip install etnltk
  ```

### From Source

- Alternatively, you can also install from source via `etnltk` git repository, which will give you more flexibility in developing on top of etltk. For this option, run

  ```python
    git clone https://github.com/robikieq/etnltk.git
    
    cd etnltk
    
    pip install -e .
  ```

## Documentation

<https://etnltk.netlify.app/>

## Usage

1. Amharic text preprocessing with Amharic document
    - Preprocessing amharic text is very simple: you can simply pass the text to the `Amharic` document and access all annotations from the returned Amharic document object:

    ```python
      from etnltk import Amharic

      sample_text = """
        ሚያዝያ 14፣ 2014 ዓ.ም 🤗 በአገር ደረጃ የሰው ሰራሽ አስተውሎት /Artificial Intelligence/ አሁን ካለበት ዝቅተኛ ደረጃ ወደ ላቀ ደረጃ ለማድረስ፣ ሃገርኛ ቋንቋዎችን ለዓለም ተደራሽ ለማድረግ፣ አገራዊ አቅምን ለማሳደግ እና ተጠቃሚ ለመሆን በጋራ አብሮ መስራቱ እጅግ ጠቃሚ ነው፡፡

        በማሽን ዓስተምሮ (Machine Learning) አማካኝነት የጽሁፍ ናሙናዎች በአርቲፊሻል ኢንተለጀንስ ሥርዓት ለማሰልጠን፣ የጽሁፍ ዳታን መሰብሰብ እና ማደራጀት፤ የናቹራል ላንጉዌጅ ፕሮሰሲንግ ቱሎችን /Natural Language Processing Tools/ በመጠቀም የጽሁፍ ዳታን ፕሮሰስ ማድረግ ተቀዳሚ እና መሰረታዊ ጉዳይ ነው።
      """
  
      # Annotating Amharic document
      doc = Amharic(sample_text)

      # print the `clean` text:
      print(doc)
      
      # output: Amharic("ሚያዝያ ዓመተ ምህረት በአገር ደረጃ የሰው ሰራሽ አስተውሎት አሁን ካለበት ዝቅተኛ ደረጃ ወደ ላቀ ደረጃ ለማድረስ ሀገርኛ ቋንቋዎችን ለአለም ተደራሽ ለማድረግ አገራዊ አቅምን ለማሳደግ እና ተጠቃሚ ለመሆን በጋራ አብሮ መስራቱ እጅግ ጠቃሚ ነው በማሽን አስተምሮ አማካኝነት የፅሁፍ ናሙናዎች በአርቲፊሻል ኢንተለጀንስ ስርአት ለማሰልጠን የፅሁፍ ዳታን መሰብሰብ እና ማደራጀት የናቹራል ላንጉዌጅ ፕሮሰሲንግ ቱሎችን በመጠቀም የፅሁፍ ዳታን ፕሮሰስ ማድረግ ተቀዳሚ እና መሰረታዊ ጉዳይ ነው")
    ```

     - Here is a another example of performing text cleaning on a piece of plaintext using `clean_amharic` function:

    ```python
    from etnltk.lang.am import (
      preprocessing,
      clean_amharic
    )

    sample_text = """
      ሚያዝያ 14፣ 2014 ዓ.ም 🤗 በአገር ደረጃ የሰው ሰራሽ አስተውሎት /Artificial Intelligence/ አሁን ካለበት ዝቅተኛ ደረጃ ወደ ላቀ ደረጃ ለማድረስ፣ ሃገርኛ ቋንቋዎችን ለዓለም ተደራሽ ለማድረግ፣ አገራዊ አቅምን ለማሳደግ እና ተጠቃሚ ለመሆን በጋራ አብሮ መስራቱ እጅግ ጠቃሚ ነው፡፡

      በማሽን ዓስተምሮ (Machine Learning) አማካኝነት የጽሁፍ ናሙናዎች በአርቲፊሻል ኢንተለጀንስ ሥርዓት ለማሰልጠን፣ የጽሁፍ ዳታን መሰብሰብ እና ማደራጀት፤ የናቹራል ላንጉዌጅ ፕሮሰሲንግ ቱሎችን /Natural Language Processing Tools/ በመጠቀም የጽሁፍ ዳታን ፕሮሰስ ማድረግ ተቀዳሚ እና መሰረታዊ ጉዳይ ነው።
    """

    # Define a custom preprocessor pipeline
    custom_pipeline = [
      preprocessing.remove_emojis, 
      preprocessing.remove_digits,
      preprocessing.remove_ethiopic_punct,
      preprocessing.remove_english_chars, 
      preprocessing.remove_punct
    ]
    
    # `clean_amharic` function takes a custom pipeline, if not uses the default pipeline
    cleaned = clean_amharic(input_text, abbrev=False, pipeline=custom_pipeline)

    # print the `clean` text:
    print(cleaned)
    # output: ሚያዝያ ዓመተ ምህረት በአገር ደረጃ የሰው ሰራሽ አስተውሎት አሁን ካለበት ዝቅተኛ ደረጃ ወደ ላቀ ደረጃ ለማድረስ ሀገርኛ ቋንቋዎችን ለአለም ተደራሽ ለማድረግ አገራዊ አቅምን ለማሳደግ እና ተጠቃሚ ለመሆን በጋራ አብሮ መስራቱ እጅግ ጠቃሚ ነው በማሽን አስተምሮ አማካኝነት የፅሁፍ ናሙናዎች በአርቲፊሻል ኢንተለጀንስ ስርአት ለማሰልጠን የፅሁፍ ዳታን መሰብሰብ እና ማደራጀት የናቹራል ላንጉዌጅ ፕሮሰሲንግ ቱሎችን በመጠቀም የፅሁፍ ዳታን ፕሮሰስ ማድረግ ተቀዳሚ እና መሰረታዊ ጉዳይ ነው
    ```

2. Tokenization - Sentence
    - Here is a simple example of performing sentence tokenization on a piece of plaintext using Amharic document:
    - Within Amharic document, annotations are further stored in `Sentences`

    ```python
    from etnltk import Amharic

    sample_text = """
      የማሽን ለርኒንግ ስልተ-ቀመሮች  (Algorithms) በመጠቀም ቋንቋዎችን መለየት እና መረዳት፣ የጽሁፍ ይዘቶችን መለየት፣ የቋንቋን መዋቅር መተንተን የሚያስችሉ የሃገሪኛ ናቹራል ላንጉዌጅ ፕሮሰሲንግ ቱሎች (NLP tools) ፣ ስልተ-ቀመሮች እና ሞዴሎችን ማዘጋጀት ተገቢ ነው። በዚህም መሰረት አማርኛ፣ አፋን ኦሮሞ፣ ሶማሊኛ እና ትግርኛ ቋንቋዎችን ለማሽን የማስተማር ሂደትን ቀላልና የተቀላተፍ እንዲሆን ያስችላል፡፡
    """

    # Annotating Amharic Text
    doc = Amharic(sample_text)

    # print all list of `Sentence` in a document:
    print(doc.sentences)
    # output: [Sentence("የማሽን ለርኒንግ ስልተቀመሮች በመጠቀም ቋንቋዎችን መለየት እና መረዳት የፅሁፍ ይዘቶችን መለየት የቋንቋን መዋቅር መተንተን የሚያስችሉ የሀገሪኛ ናቹራል ላንጉዌጅ ፕሮሰሲንግ ቱሎች ስልተቀመሮች እና ሞዴሎችን ማዘጋጀት ተገቢ ነው"), Sentence("በዚህም መሰረት አማርኛ አፋን ኦሮሞ ሶማሊኛ እና ትግርኛ ቋንቋዎችን ለማሽን የማስተማር ሂደትን ቀላልና የተቀላተፍ እንዲሆን ያስችላል")]
    ```

    - Here is another example of performing sentence tokenization on a piece of plaintext using `sentence_tokenize` function:

    ```python
    from etnltk.tokenize.am import sent_tokenize

    sample_text = """
      የማሽን ለርኒንግ ስልተ-ቀመሮች  (Algorithms) በመጠቀም ቋንቋዎችን መለየት እና መረዳት፣ የጽሁፍ ይዘቶችን መለየት፣ የቋንቋን መዋቅር መተንተን የሚያስችሉ የሃገሪኛ ናቹራል ላንጉዌጅ ፕሮሰሲንግ ቱሎች (NLP tools) ፣ ስልተ-ቀመሮች እና ሞዴሎችን ማዘጋጀት ተገቢ ነው። በዚህም መሰረት አማርኛ፣ አፋን ኦሮሞ፣ ሶማሊኛ እና ትግርኛ ቋንቋዎችን ለማሽን የማስተማር ሂደትን ቀላልና የተቀላተፍ እንዲሆን ያስችላል፡፡
    """

    # Annotating a Document
    sentences = sent_tokenize(sample_text)

    # print all list of sentence:
    print(sentences)
    # output: ['የማሽን ለርኒንግ ስልተቀመሮች በመጠቀም ቋንቋዎችን መለየት እና መረዳት የፅሁፍ ይዘቶችን መለየት የቋንቋን መዋቅር መተንተን የሚያስችሉ የሀገሪኛ ናቹራል ላንጉዌጅ ፕሮሰሲንግ ቱሎች ስልተቀመሮች እና ሞዴሎችን ማዘጋጀት ተገቢ ነው', 'በዚህም መሰረት አማርኛ አፋን ኦሮሞ ሶማሊኛ እና ትግርኛ ቋንቋዎችን ለማሽን የማስተማር ሂደትን ቀላልና የተቀላተፍ እንዲሆን ያስችላል']

3. Tokenization - Word
    - Here is a simple example of performing word tokenization on a piece of plaintext using AmharicDocument:
    - Within Amharic focument, annotations are further stored in `Words`.

    ```python
    from etnltk import AmharicDocument

    sample_text = """
      “ተረኛ፣ ተረኛ!” አለ ነርሱ። ወይዘሮ
      ታሪኳ፣ “አቤት!” ብለው የሁለት
      ዓመት ልጃቸውን ይዘው ገቡ።
      “ምኑን ነው ያመመው?” ዶክተሯ
      ጠየቁ። “አያዩትም! ፀጉሩ ሳስቷል፤
      ሆዱ ተነፍቷል፤ ድዱም ይደማል”
      አሉ ወይዘሮ ታሪኳ። ዶክተሯም፣
      “በጣም ያሳዝናል፤ እንደዚህ
      ያደረገው የተመጣጠነ ምግብ አለማግኘቱ ነው። አሁንም ወተት፣
      እንቁላል፣ ማር፣ አትክልትና ፍራፍሬ ይመግቡት፤ ቶሎ ይሻለዋል፤
      ለአሁኑ ግን መድኃኒት አዝለታለሁ” በማለት አስረዷቸው። ወይዘሮ
      ታሪኳም “ወይ አለማወቅ! ልጄን በምግብ እጥረት ገድዬው ነበር"
      በማለት አለቀሱ።

      """
    
    # Annotating Amharic Text
    doc = Amharic(sample_text)

    # print all list of `AmharicWord` in a document:
    print(doc.words)
    # output: ['ተረኛ', 'ተረኛ', 'አለ', 'ነርሱ', 'ወይዘሮ', 'ታሪኳ', 'አቤት', 'ብለው', 'የሁለት', 'አመት', 'ልጃቸውን', 'ይዘው', 'ገቡ', 'ምኑን', 'ነው', 'ያመመው', 'ዶክተሯ', 'ጠየቁ', 'አያዩትም', 'ፀጉሩ', 'ሳስቷል', 'ሆዱ', 'ተነፍቷል', 'ድዱም', 'ይደማል', 'አሉ', 'ወይዘሮ', 'ታሪኳ', 'ዶክተሯም', 'በጣም', 'ያሳዝናል', 'እንደዚህ', 'ያደረገው', 'የተመጣጠነ', 'ምግብ', 'አለማግኘቱ', 'ነው', 'አሁንም', 'ወተት', 'እንቁላል', 'ማር', 'አትክልትና', 'ፍራፍሬ', 'ይመግቡት', 'ቶሎ', 'ይሻለዋል', 'ለአሁኑ', 'ግን', 'መድሀኒት', 'አዝለታለሁ', 'በማለት', 'አስረዷቸው', 'ወይዘሮ', 'ታሪኳም', 'ወይ', 'አለማወቅ', 'ልጄን', 'በምግብ', 'እጥረት', 'ገድዬው', 'ነበር', 'በማለት', 'አለቀሱ']
    ```

    - Here is another example of performing word tokenization on a piece of plaintext using `word_tokenize` function:

    ```python
    from etnltk.tokenize.am import word_tokenize

    sample_text = """
      “ተረኛ፣ ተረኛ!” አለ ነርሱ። ወይዘሮ
      ታሪኳ፣ “አቤት!” ብለው የሁለት
      ዓመት ልጃቸውን ይዘው ገቡ።
      “ምኑን ነው ያመመው?” ዶክተሯ
      ጠየቁ። “አያዩትም! ፀጉሩ ሳስቷል፤
      ሆዱ ተነፍቷል፤ ድዱም ይደማል”
      አሉ ወይዘሮ ታሪኳ። ዶክተሯም፣
      “በጣም ያሳዝናል፤ እንደዚህ
      ያደረገው የተመጣጠነ ምግብ አለማግኘቱ ነው። አሁንም ወተት፣
      እንቁላል፣ ማር፣ አትክልትና ፍራፍሬ ይመግቡት፤ ቶሎ ይሻለዋል፤
      ለአሁኑ ግን መድኃኒት አዝለታለሁ” በማለት አስረዷቸው። ወይዘሮ
      ታሪኳም “ወይ አለማወቅ! ልጄን በምግብ እጥረት ገድዬው ነበር"
      በማለት አለቀሱ።

    """
      
    # word tokenization
    words = word_tokenize(sample_text)

    # print all list of word:
    print(words)
    # output: ['ተረኛ', 'ተረኛ', 'አለ', 'ነርሱ', 'ወይዘሮ', 'ታሪኳ', 'አቤት', 'ብለው', 'የሁለት', 'አመት', 'ልጃቸውን', 'ይዘው', 'ገቡ', 'ምኑን', 'ነው', 'ያመመው', 'ዶክተሯ', 'ጠየቁ', 'አያዩትም', 'ፀጉሩ', 'ሳስቷል', 'ሆዱ', 'ተነፍቷል', 'ድዱም', 'ይደማል', 'አሉ', 'ወይዘሮ', 'ታሪኳ', 'ዶክተሯም', 'በጣም', 'ያሳዝናል', 'እንደዚህ', 'ያደረገው', 'የተመጣጠነ', 'ምግብ', 'አለማግኘቱ', 'ነው', 'አሁንም', 'ወተት', 'እንቁላል', 'ማር', 'አትክልትና', 'ፍራፍሬ', 'ይመግቡት', 'ቶሎ', 'ይሻለዋል', 'ለአሁኑ', 'ግን', 'መድሀኒት', 'አዝለታለሁ', 'በማለት', 'አስረዷቸው', 'ወይዘሮ', 'ታሪኳም', 'ወይ', 'አለማወቅ', 'ልጄን', 'በምግብ', 'እጥረት', 'ገድዬው', 'ነበር', 'በማለት', 'አለቀሱ']

4. Normalization
    1. Character Level Normalization such as "`ጸ`ሀይ" and "`ፀ`ሐይ"
    2. Labialized Character Normalzation such as "ሞል`ቱዋ`ል" to "ሞል`ቷ`ል"
    3. Short Form Expansion such as "`አ.አ`" to "`አዲስ አበባ`"
    4. Punctuation Normalization such as `::` to `።`

    - Here is a simple example of performing normalization on a piece of plaintext using `normalize` function:

    ```python
    from etnltk.lang.am import normalize

    sample_text = """
      ሚያዝያ 14፣ 2014 ዓ.ም በዓገር ደረጃ የሰው ሰራሽ አስተውሎት የውይይት መድረክ ላይ
      የሃገርኛ ቋንቋዎች ትርጉም አገልግሎት፣ 
      ቻትቦት (የውይይት መለዋወጫ ሮቦት): 
      የፅሁፍ ሰነዶች ለመለየት፣ የቃላት ትክክለኛነትን ለማረጋገጥ፣ 
      በቋንቋን ሕግጋት መሠረት ጽሑፎችን ለማዋቀር እና ለመመስረት፣ 
      ረጅም ጽሁፎችን ለማሳጠር፣ አንኳር ጉዳዮችን መለየት ወይም ጥቅል ሃሳብ ለማውጣት፣ 
      ንግግርን ወደ ጽሁፍ ለመቀየር የሚያስችሉ መተግበሪያዎችን ማልማት አስረላጊነቱ ተገልጹዋል::
    """

    # normalization
    normalized_text = normalize(sample_text)

    # The following example shows how to print all normalized in a document:
    print(normalized_text)
    # output: ሚያዝያ 14፣ 2014 አመተ ምህረት በአገር ደረጃ የሰው ሰራሽ አስተውሎት የውይይት መድረክ ላይ
    # የሀገርኛ ቋንቋዎች ትርጉም አገልግሎት፣ 
    # ቻትቦት (የውይይት መለዋወጫ ሮቦት)፡ 
    # የፅሁፍ ሰነዶች ለመለየት፣ የቃላት ትክክለኛነትን ለማረጋገጥ፣ 
    # በቋንቋን ህግጋት መሰረት ፅሁፎችን ለማዋቀር እና ለመመስረት፣ 
    # ረጅም ፅሁፎችን ለማሳጠር፣ አንኳር ጉዳዮችን መለየት ወይም ጥቅል ሀሳብ ለማውጣት፣ 
    # ንግግርን ወደ ፅሁፍ ለመቀየር የሚያስችሉ መተግበሪያዎችን ማልማት አስረላጊነቱ ተገልጿል። """
    ```

    - Here is another example of performing normalization on a piece of plaintext using `normalize_char`, `normalize_punct`, `normalize_labialized`, `normalize_shortened` function:

    ```python
    from etnltk.lang.am.normalizer import ( 
      normalize_labialized, 
      normalize_shortened,
      normalize_punct,
      normalize_char
    )

    # normalize labialized 
    normalized_text = normalize_labialized("ንግግርን ወደ ጽሁፍ ለመቀየር የሚያስችሉ መተግበሪያዎችን ማልማት አስረላጊነቱ ተገልጹዋል")
    print(normalized_text)
    # output: ንግግርን ወደ ፅሁፍ ለመቀየር የሚያስችሉ መተግበሪያዎችን ማልማት አስረላጊነቱ ተገልጿል

    # normalize short forms
    normalized_text = normalize_shortened("ሚያዝያ 14፣ 2014 ዓ.ም በዓገር ደረጃ የሰው ሰራሽ አስተውሎት የውይይት መድረክ")
    print(normalized_text)
    # output: ሚያዝያ 14፣ 2014 ዓመተ ምህረት በአገር ደረጃ የሰው ሰራሽ አስተውሎት የውይይት መድረክ

    # normalize punctuation
    normalized_text = normalize_punct("መተግበሪያዎችን ማልማት አስረላጊነቱ ተገልጹዋል::")
    print(normalized_text)
    # output: መተግበሪያዎችን ማልማት አስረላጊነቱ ተገልጿል።

    # normalize characters
    normalized_text = normalize_char("በቋንቋዉ ሕግጋት መሠረት ጽሑፎችን ማዋቀር እና መመሥረት")
    print(normalized_text)
    # output: በቋንቋዉ ህግጋት መሰረት ፅሁፎችን ማዋቀር እና መመስረት

## Features

- Text preprocessing functions.

    ``` python
    from etnltk.lang.am import preprocessing
    ```

    | Function | Description |
    -----------|-------------|
    | remove_whitespaces | Remove extra spaces, tabs, and new lines from a text string
    | remove_links | Remove URLs from a text string
    | remove_tags | Remove HTML tags from a text string
    | remove_emojis | Remove emojis from a text string
    | remove_email | Remove email adresses from a text string
    | remove_digits | Remove all digits from a text string
    | remove_english_chars | Remove ascii characters from a text string
    | remove_arabic_chars | Remove arabic characters and numerals from a text string
    | remove_chinese_chars | Remove chinese characters from a text string
    | remove_ethiopic_digits | Remove all ethiopic digits from a text string
    | remove_ethiopic_punct | Remove ethiopic punctuations from a text string
    | remove_non_ethiopic | Remove non ethioipc characters from a text string
    | remove_stopwords | Remove stop words
