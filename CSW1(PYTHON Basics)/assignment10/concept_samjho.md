# Assignment 10: Pandas and Matplotlib 📊🐼

Bhai, data science aur analytics ki aadhi zindagi sirf in 2 modules pe chalti hai: **Pandas (Data manipulation)** aur **Matplotlib (Data Visualization)**.

Kyun use karte hain?
Jab hazaaro ya lakho rows/columns ka data ho, tab normal list/array se handle karna impossible hota hai. `Pandas` data ko Table (Excel jaise) mein organise karta hai. Aur insaan directly numbers dekh kar pattern nahi samajhte, unhe Graph/Chart chaiye... Yeh graph banane ka field `Matplotlib` sambhalta hai!

---

### 1. Pandas kya hai aur DataFrame kya hota hai? (Questions 1 - 5)
Pandas Excel-sheet jaisa tool hai. Data 2D tables mein shift hota hai jise **DataFrame** bolte hain.

- **DataFrame Creation (Q1):** Normal Data Dictionary passing karke `pd.DataFrame(data)` data ko table format mein properly arrange kar deta hai.
- **Viewing Data (Q2):** Agar hamare paas lakho rows hai toh `df.head(5)` sirf upar ki 5 rows display karta hai verify karne ke liye taake system par load na aaye, and `df.describe()` poore data ke statistics bata deta hai.
- **Filtering (Q3):** Tu easily pure column main math logic laga sakta hai! Jaise `df[df['Marks'] > 50]`, bas single line me sab pass wale filter ho jayenge!
- **Handling Missing Values (NaN) (Q4):** Asli data main boht missing values hoti hain (Nulls). Unko fill karna boht issue hota h pr pandas me `df.fillna()` single line lagate hi empty spaces bhari jati hain!
- **GroupBy (Q5):** Ye SQL `GROUP BY` logic pe chalta hai. Agar IT & HR department data mixed hai toh `df.groupby('Department')` dono ki mapping sum/average directly alag alag perform karega!

---

### 2. Matplotlib (Graphs ka Baadshah) 📉 (Questions 6 - 9)

Table ka backend graph banana module coordinate plotting karna hotaa hai. Isko `import matplotlib.pyplot as plt` code import me laya jata h.

- **Line Chart (Q6):** Timeline sequence ya past history display krani toh use `plt.plot(x, y)`.
- **Bar Chart (Q7):** Multiple categories/groups compare karna ho then best command `plt.bar()` rehti hai!
- **Scatter Plot (Q8):** Do items (like Weight aur Height) ka corellation check ho na to map points ke format scatter dot form main banti hai bina line ke, via `plt.scatter(x,y)`.
- **Histogram (Q9):** Kisi numerical density ya bins Distribution check krni ho range values  `plt.hist(data)` map se.
- ***Important Note:*** Graph backend pe save toh hota hi per GUI (Visual window popup) show krane code me explicitly command chalana parega `plt.show()` tb plot dikhegay code exectue hotey vakt! (Meri q files me show() comment kiya hai taaki run main rukawat na ho. Tum uncomment de dena display k lie).

---

### 3. Ultimate Combo: Pandas + Matplotlib (Question 10)
Donou libraries separate use karoge toh data mapping array conversion pain deti h, But these libraries internally coupled design setup kyi gayi hain. DataFrame structure directly function provide karti h plotting ke : 
Jaise  `df.plot(kind='line')`. Data alag alag module main pass kara ne k bijay , pandas internally Matplotlib ko feed send kar direct visualization show kardeta h without separate explicit mappings setup ! 
