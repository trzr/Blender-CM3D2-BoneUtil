# Blender-CM3D2-BoneUtil
　本アドオンは、「[カスタムメイド3D2](http://kisskiss.tv/cm3d2/)」向けモデルデータのボーンに関連した補助機能を提供します。  
  モデルデータの扱いは、[CM3D2 Converter](https://github.com/CM3Duser/Blender-CM3D2-Converter)の使用を前提としています。

　**本アドオンは、不具合が残っている可能性があります。**  
　使用前にデータのバックアップを取っておくようお願いします。  

### ■ インストール (Installation)
##### ◇事前準備
　Blender2.76以上(動作確認は[2.77a](http://download.blender.org/release/Blender2.77/))がインストールされており[日本語化]している事が前提です。

##### ◇ダウンロード・展開
　画面右の「[Download ZIP](https://github.com/trzr/Blender-CM3D2-BoneUtil/archive/master.zip)」からファイルをダウンロード・解凍し、  
> %APPDATA%\Blender Foundation\Blender\%{Version}\scripts\addons\  

に配置してください。  
例) Windows7、Blender-2.77a、ユーザ「UserA」の場合  
>C:\Users\UserA\AppData\Roaming\Blender Foundation\Blender\2.77\scripts\addons\CM3D2 BoneUtil\*.py

   に配置する形になります。  
   もし、フォルダが存在しない場合は作成してください。

##### ◇設定
　Blenderを起動し、ユーザー設定のアドオンタブで「cm3d2」等で検索し、  
　「Tools: CM3D2 BoneUtil」をオンにすれば(一時的に)有効になります。  
　次回起動時からも有効にしたい場合は「ユーザー設定の保存」をクリックして下さい。  

### ■ 機能
##### ◇BoneData取り込み機能  
 [機能説明](https://github.com/trzr/Blender-CM3D2-BoneUtil/wiki/%E6%A9%9F%E8%83%BD%E8%AA%AC%E6%98%8E)を参照

<!--
##### ◇ボーン名一括リネーム
　揺れボーンの型を一括で変更する機能

##### ◇疑似ボーンメッシュ
  ボーンの位置をなぞったメッシュを作成する機能
-->

### ■ 免責
  本アドオンの使用または使用不能から生じるいかなる損害について、作者は一切の責任を負えません。  
  各自の責任において使用してください。

### ■ その他
  基本となる計算式は、[夜勤D](https://github.com/yknD-CM3D2)さんの作成されたスクリプトをベースにしております。   
  また、アドオンは、さいでんかさんの[CM3D2 Converter](https://github.com/CM3Duser/Blender-CM3D2-Converter)を参考にさせていただきました。  
  感謝！
