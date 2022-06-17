# OIT Syllabus App

<img src="https://raw.githubusercontent.com/yashikota/OIT-Tools_syllabus/master/web/public/icon.webp" width="50%" alt="ロゴ">

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/yashikota/OIT-Tools_syllabus?label=version&style=plastic)
[![Scraping](https://github.com/yashikota/OIT-Tools_syllabus/actions/workflows/Scraping.yaml/badge.svg)](https://github.com/yashikota/OIT-Tools_syllabus/actions/workflows/Scraping.yaml)  

<text>

大阪工業大学**非公式**のシラバスアプリです  
2022/06/13
時点での
[大阪工業大学公式シラバス](https://www.oit.ac.jp/japanese/syllabus/index.html)
のデータに基づきます  
各自で必ず公式シラバスも合わせて確認してください  
**iOS15.2未満のバージョンでは表示に不具合が出る可能性があります。不具合が発生した場合はiOSのバージョンを15.2以上にした上でご利用ください**  
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
[Jin](https://github.com/MatsuJin000)  

本アプリケーションに記載されている情報の正確性、最新性、有用性等その他一切の事項について、いかなる保証をするものではありません  
このような場合において、記載が不正確であったこと等により生じた、いかなる損害に関しても、一切の責任を負いかねます  
また、本アプリケーションではアクセス状況の把握やサイト改善に役立てるため、Google Analytics及びCloudflare Web Analyticsを利用しています  
[知的財産の表記](https://raw.githubusercontent.com/yashikota/OIT-Tools_syllabus/master/web/public/hyouki.txt)

</text>

## 使い方

<img src="https://raw.githubusercontent.com/yashikota/OIT-Tools_syllabus/master/web/src/ss.webp" alt="トップ画面">

<text>

①OIT-Toolsホームページへのリンクになってます  
②使い方やプログラムの説明をしているこのページ  
③タップするとライトテーマ・ダークテーマを切り替えます  
④表示するシラバスの年度を指定できます  
⑤テーブル全体の要素を検索します  
⑥昇順降順のソートを切り替えます  
⑦この下の列だけを検索します。各列の検索結果は重複して適応可能です  
⑧プルダウンメニューで絞り込みができます  
⑨公式シラバスの該当するページを表示します  
⑩表示する行数を変更できます  
⑪一番最初のページに戻る  
⑫一つ前のページに戻る  
⑬一つ次のページに進む  
⑭一番最後のページに進む  

※ホーム画面への追加方法は以下のリンクをご参照ください  
[iOS・Androidの追加方法](https://support.bccks.jp/faq/pwa_2020/)
(手順1は飛ばす)  
[PC(Chrome・Edge)の追加方法](https://support.google.com/chrome/answer/9658361)  

</text>

## Q&A

## プログラムの説明

<text>

下にあるディレクトリ構造を見ながら読むとわかりやすいかも

</text>

### Tool

<text>

・extract.py  
2通りのアプローチをして講義コードを抽出している  
①時間割PDFを画像に変換し、画像から講義コードを抜き出した画像を生成し、その画像をOCRしたものをcsvに保存  
OCRにはTesseractを利用しているため別途インストールが必要。学習データは
[これ](https://github.com/tesseract-ocr/tessdata_best/blob/main/eng.traineddata)
を利用している  
②pdfminer.sixを使いPDFからテキストデータを抽出し、正規表現で英数字8桁のみを保存する処理を行う  
この2つを組み合わせることで精度を高めている  

・scraping.py  
csvから講義コードを読み込み、公式のシラバスからスクレイピングし、結果をjsonに保存  

・scraping2.py  
pandasを用いたスクレイピング。これにより掲載されている全要素を取得することができるようになった。

### Web

React+MUI+Material-Tableで構築  
Cloudflare Pagesにホスティング  

・public  
ライセンス表記ファイルやファビコンファイル等を格納している  

・/components  
コンポーネントを格納している

・202*.json  
表示しているシラバスの全データが入ったjson  

・202*mini.json  
容量制限回避のため、一部要素のみが入ったjson  

</text>

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
│   ├── convert.py
│   ├── extract.py
│   ├── requirements.txt
│   ├── scraping.py
│   ├── scraping2.py
│   └── timetable
│       ├── 2021
│       │   ├── csv
│       │   ├── num
│       │   ├── numbers.csv
│       │   ├── pdf
│       │   └── png
│       ├── 2022
│       │   ├── csv
│       │   ├── num
│       │   ├── numbers.csv
│       │   ├── omiya-oneline.csv
│       │   ├── omiya-only.csv
│       │   ├── omiya-original.csv
│       │   ├── omiya.csv
│       │   ├── pdf
│       │   └── png
│       └── poppler
└── web
    ├── .gitignore
    ├── package-lock.json
    ├── package.json
    ├── public
    │   ├── favicon.ico
    │   ├── hyouki.txt
    │   ├── icon.webp
    │   ├── index.html
    │   ├── manifest.json
    │   └── robots.txt
    ├── server.js
    ├── src
    │   ├── App.tsx
    │   ├── components
    │   │   ├── About.tsx
    │   │   ├── Header.tsx
    │   │   └── Table.tsx
    │   ├── data
    │   │   ├── 2021.json
    │   │   ├── 2021mini.json
    │   │   ├── 2022.json
    │   │   └── 2022mini.json
    │   ├── index.tsx
    │   ├── react-app-env.d.ts
    │   ├── service-worker.ts
    │   ├── serviceWorker
    │   │       Registration.ts
    │   └── ss.webp
    └── tsconfig.json
</pre>

<!-- エラー数=1106 -->