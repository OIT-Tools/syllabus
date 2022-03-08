# OIT Syllabus App

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/yashikota/OIT-Tools_syllabus?label=version&style=plastic)
[![Scraping](https://github.com/yashikota/OIT-Tools_syllabus/actions/workflows/Scraping.yaml/badge.svg)](https://github.com/yashikota/OIT-Tools_syllabus/actions/workflows/Scraping.yaml)  

大阪工業大学**非公式**のシラバスアプリです  
2022/03/08
時点での
[大阪工業大学公式シラバス](https://www.oit.ac.jp/japanese/syllabus/index.html)
のデータに基づきます  
各自で必ず公式シラバスも合わせて確認してください  
バグ、データの不備、機能要望、その他問い合わせは
[Google Forms](https://docs.google.com/forms/d/e/1FAIpQLSc08BgQQiNqXeFjcECLKlfzmoOygvv1gglc_j7xnGdUmBeYLg/viewform?usp=sf_link)
か
[GitHub issues](https://github.com/yashikota/OIT-Tools_syllabus/issues)
のどちらかにお願いします  
アプリケーションは
[syllabus.oit.yashikota.com](https://syllabus.oit.yashikota.com)
で、ソースコードは
[GitHub](https://github.com/yashikota/OIT-Tools_syllabus)
で公開してます  
Contributed by
[kota](https://github.com/yashikota)
[aoken](https://github.com/aoken7)
[Akirtn](https://github.com/Akirtn)
[maru](https://github.com/GenichiMaruo)  

本アプリケーションに記載されている情報の正確性、最新性、有用性等その他一切の事項について、いかなる保証をするものではありません  
このような場合において、記載が不正確であったこと等により生じた、いかなる損害に関しても、一切の責任を負いかねます  
また、本アプリケーションではアクセス状況の把握やサイト改善に役立てるため、Google Analytics及びCloudflare Web Analyticsを利用しています  
[知的財産の表記](https://raw.githubusercontent.com/yashikota/OIT-Tools_syllabus/master/web/public/hyouki.txt)

## 使い方

<img src="https://raw.githubusercontent.com/yashikota/OIT-Tools_syllabus/master/web/src/ss.webp" alt="トップ画面">

①OIT-Toolsホームページへのリンクになってます  
②使い方やプログラムの説明をしているこのページ  
③タップするとライトテーマ・ダークテーマを切り替えます  
④タップするとテーブルの一番上の行に戻ります  
⑤テーブル全体の要素を検索します  
⑥昇順降順のソートを切り替えます  
⑦この下の列だけを検索します。各列の検索結果は重複して適応可能  
⑧プルダウンメニューで絞り込みができます  
⑨公式シラバスの該当するページを表示します  

※ホーム画面への追加方法は以下のリンクをご参照ください  
[iOS・Androidの追加方法](https://support.bccks.jp/faq/pwa_2020/)
(手順1は飛ばす)  
[PC(Chrome・Edge)の追加方法](https://support.google.com/chrome/answer/9658361)  

## Q&A

## プログラムの説明

下にあるディレクトリ構造を見ながら読むとわかりやすいかも

### Tool

・extract.py  
時間割PDFを画像に変換し、画像から講義コードを抜き出した画像を生成し、その画像をOCRしたものをCSVに保存  
OCRにはTesseractを利用しているため別途インストールが必要。学習データは
[これ](https://github.com/tesseract-ocr/tessdata_best/blob/main/eng.traineddata)
を利用している  
・pdfconvert.py  
時間割PDFからテキストを抽出して正規表現で講義コードのみをCSVに保存  
・scraping.py  
CSVから講義コードを読み込み、公式のシラバスからスクレイピングし、結果をJSONに保存  
・numbers.csv  
スクレイピングの際にできる副産物のような物。今の所使用する予定はない  

### Web

React+MUI+Material-Tableで構築  
Cloudflare Pagesにホスティング  

・public  
ライセンス表記ファイルやファビコンファイル等を格納している  
・src  
主にソースコードを格納している  
・components  
今回使用しているReactというライブラリはコンポーネント指向という考え方に基づいて開発されている。  
ファイル名を見て分かる通り、Header.tsxはヘッダー、Table.tsxはテーブル（シラバスデータを表示しているもの）といった感じで部品ごとにソースコードが分けられている。  
これのメリットは機能単位で分けられているためメンテナンスがしやすいことや違うプロジェクトでも使い回しが容易であることが挙げられる  
・202*.json  
表示しているシラバスの全データが入ったJSONファイル。利用はご自由にどうぞ  

### ディレクトリ構造

<pre>
.
├── .github
│   └── workflows
│       ├── Lighthouse.yaml
│       └── Scraping.yaml
├── .lighthouserc.js
├── README.md
├── tool
│   ├── .gitignore
│   ├── extract.py
│   ├── pdfconvert.py
│   ├── requirements.txt
│   ├── scraping.py
│   ├── timetable
│   │   ├── 2021
│   │   │   ├── csv
│   │   │   ├── num
│   │   │   ├── numbers.csv
│   │   │   ├── pdf
│   │   │   └── png
│   │   └── poppler
└── web
    ├── .gitignore
    ├── package-lock.json
    ├── package.json
    ├── public
    │   ├── hyouki.txt
    │   ├── index.html
    │   ├── manifest.json
    │   ├── icon.webp
    │   └── robots.txt
    ├── server.js
    ├── src
    │   ├── App.tsx
    │   ├── components
    │   │   ├── About.tsx
    │   │   ├── Header.tsx
    │   │   └── Table.tsx
    │   ├── data
    │   │   └── 2021.json
    │   ├── index.tsx
    │   ├── react-app-env.d.ts
    │   ├── service-worker.ts
    │   ├── serviceWorker
    │   │       Registration.ts
    │   └── ss.webp
    └── tsconfig.json
</pre>

<!-- エラー数=2101 -->