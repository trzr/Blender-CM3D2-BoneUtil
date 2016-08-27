# Blender-CM3D2-BoneUtil
---
　本アドオンは、「[カスタムメイド3D2](http://kisskiss.tv/cm3d2/)」向けモデルデータのボーンに関連した補助機能を提供します。  
  モデルデータの扱いは、[CM3D2 Converter](https://github.com/CM3Duser/Blender-CM3D2-Converter)の使用を前提としています。

　**本アドオンは、不具合が残っている可能性があります。**  
　使用前のデータバックアップを推奨

## ■ インストール (Installation)
#### ◇事前準備
　Blender2.76以上(動作確認は[2.77a](http://download.blender.org/release/Blender2.77/))がインストールされていることが前提です。

#### ◇ダウンロード・展開
　画面右の「[![ダウンロードボタン][img_download]][master zip]」か、  
[Release](https://github.com/trzr/Blender-CM3D2-BoneUtil/releases)のリンク先にある該当該当のバージョン  
からファイルをダウンロード・解凍し、  

```
 %APPDATA%\Blender Foundation\Blender\{Version}\scripts\addons\  
 ```
に配置してください。  
例) Windows7、Blender-2.77a、ユーザ「UserA」の場合  
```
C:\Users\UserA\AppData\Roaming\Blender Foundation\Blender\2.77\scripts\addons\CM3D2 BoneUtil\*.py
```
   に配置する形になります。  
   もし、フォルダが存在しない場合は作成してください。

#### ◇設定
　Blenderを起動し、ユーザー設定のアドオンタブで「cm3d2」等で検索し、  
　「Tools: CM3D2 BoneUtil」をオンにすれば(一時的に)有効になります。  
　次回起動時からも有効にしたい場合は「ユーザー設定の保存」をクリックして下さい。  


## ■ 機能

### ◇ [BoneData取り込み機能](https://github.com/trzr/Blender-CM3D2-BoneUtil/wiki/Import%20To%20BoneData)  
　Blender上のボーンからBoneDataを取込む機能

### ◇ [揺れボーンタイプ 一括変更機能](https://github.com/trzr/Blender-CM3D2-BoneUtil/wiki/Change%20BoneType)（オプション）  
　揺れボーンの型を一括で変更する機能

### ◇ [シェイプキー値反映機能](https://github.com/trzr/Blender-CM3D2-BoneUtil/wiki/BlendsetImporter)
　blendsetを元に、シェイプキーの値を一括で変更する機能



## ■ 免責
  本アドオンの使用または使用不能から生じるいかなる損害について、作者は一切の責任を負えません。  
  各自の責任において使用してください。

## ■ 謝辞
  ボーンの計算式は、[夜勤D](https://github.com/yknD-CM3D2)さんの作成されたスクリプトをベースにさせていただいております。   
  また、アドオン作成は、[CM3D2 Converter](https://github.com/CM3Duser/Blender-CM3D2-Converter)を参考にさせていただきました。  
  感謝！
