
dic = {
	"en_US" : {
		("*", "Add") : "add",
		("*", "Import") : "Import",
		("*", "Export") : "Export",
		("*", "Scale") : "scale",
		("*", "Hardness") : "hardness",
		("*", "BoneType") : "bone type",
		
		("*", "butl.AddonDesc") : "This addon is bone-utility for Custom-Maid 3D2",
		("*", "butl.EnableOption") : "Enable features",
		("*", "butl.PushSaveButton") : "Please push button \"Save User Setting\" for save option",
		("*", "butl.BaseBoneName") : "BaseBone",
		("*", "butl.RenameBone") : "rename bone on armature",
		("*", "butl.EnumAll") : "All bones",
		("*", "butl.EnumSelected") : "Only Selected",
		("*", "butl.EnumDescendant") : "Selected And Descendants",
		("*", "butl.Target") : "Target bones",
		("*", "butl.ImportTarget:") : "ImportTarget:",
		("*", "butl.ScaleDesc") : "specify scale value",
		("*", "butl.VertexGroup") : "Vertex Groups",
		("*", "butl.VertexGroup:") : "Vertex Groups:",
		("*", "butl.bdimport.ImportBoneData4CM3D2") : "for CM3D2",
		("*", "butl.bdimport.ImportBoneData") : "Import To BoneData",
		("*", "butl.bdimport.ImportBoneDataDesc") : "Convert blender's bone objects to BoneData for CM3D2",
		("*", "butl.bdimport.RenameBaseBone") : "rename BaseBone",
		("*", "butl.bdimport.RenameBaseBoneDesc") : "rename BaseBone on custom-properties",
		("*", "butl.bdimport.RenameBaseBoneCompleted") : "BaseBone has renamed",
		("*", "butl.bdimport.RemoveBoneDataNonExistent") : "Remove  BoneData (non-existent bone)",
		("*", "butl.bdimport.ExcludeIKBoneDataForRemove") : "Exclude IK-bone for remove",
		("*", "butl.bdimport.UseExist") : "use existing",
		("*", "butl.bdimport.AddVGDesc") : "add vertex-group",
		("*", "butl.bdimport.UseExistDesc") : "use only existing vertex-group",
		("*", "butl.bdimport.ImportCompleted") : "Imort completed",
		("*", "butl.bdimport.ActionMode:") : "action mode:",
		("*", "butl.bdimport.NormalMode") : "normal mode",
		("*", "butl.bdimport.AutoDetect") : "auto detect mode",
		("*", "butl.bdimport.OldMode") : "old mode",
		("*", "butl.bdimport.NormalModeDesc") : "support for Converter 0.423 or later",
		("*", "butl.bdimport.AutoDetectDesc") : "auto detect (imperfect)",
		("*", "butl.bdimport.OldModeDesc") : "support for Converter 0.414 or earlier",
		("*", "butl.ChangeBoneTypeFeature") : "Change bone-type",
		("*", "butl.ChangeBoneTypeFDesc") : "this feature change bone-types as a whole",
		("*", "butl.ChangeBoneType4CM3D2") : "Change bone-type for CM3D2",
		("*", "butl.ChangeBoneType") : "Change bone type",
		("*", "butl.ChangeBoneTypeCompleted") : "Bone-type change completed",
		("*", "butl.BoneList") : "Bone List",
		("*", "butl.GenMeshFromBoneFeature") : "generate mesh from bones",
		("*", "butl.GenMeshFromBoneFDesc") : "this feature generate mesh from bones",
		("*", "butl.GenMeshFromBone") : "Generate mesh from bones",
		("*", "butl.GenMeshFromBoneDesc") : "Generate mesh ",
		("*", "butl.ObjectName") : "Object Name",
		("*", "butl.Vertices") : "Vertices",
		("*", "butl.VerticesDesc") : "specify cylinder vertices",
		("*", "butl.Radius") : "Radius",
		("*", "butl.RadiusDesc") : "Specify cylinder radius",
		("*", "butl.EnumLocalBone") : "Only LocalBone",
		("*", "butl.EnumNone") : "No Filter",
		("*", "butl.LocalBoneDesc") : "Filtered by LocalBoneData",
		("*", "butl.EnumNoneDesc") : "No filer",
		("*", "butl.CylinderSize:") : "Cylinder size",
		("*", "butl.ImportSource:") : "Import source:",
		("*", "butl.shapekey.BatchOperation") : "ShapeKey Operations",
		("*", "butl.shapekey.CopySet") : "Copy Set",
		("*", "butl.shapekey.PasteSet"): "Paste Set",
		("*", "butl.shapekey.ClearSet"): "Clear Set",
		("*", "butl.shapekey.CopyValue") : "Copy Val",
		("*", "butl.shapekey.PasteValue") : "Paste Val",
		("*", "butl.shapekey.BlendsetOpeation") : "Blendset Opr",
		("*", "butl.shapekey.BlendsetList") : "Blendset List",
		("*", "butl.shapekey.ShapeKeyVal") : "ShapeKey Value",
		("*", "butl.shapekey.Reflect") : "Reflect",
		("*", "butl.shapekey.Regist") : "Overwrite",
		("*", "butl.shapekey.PasteBlendsets") : "paste blendset-list to custom-properties from clipboard",
		("*", "butl.shapekey.PasteBlendsets.Desc") : "paste blendset-list to custom-properties from clipboard",
		("*", "butl.shapekey.PasteBlendsets.Finished") : "Blendset-list has pasted to custom-properties. num:%d ",
		("*", "butl.shapekey.ParseFailed") : "failed to parse. skip shapekey(%s).",
		("*", "butl.shapekey.CopyBlendsets") : "copy blendset-list to clipboard from custom-properties",
		("*", "butl.shapekey.CopyBlendsets.Desc") : "copy blendset-list to clipboard from custom-properties",
		("*", "butl.shapekey.CopyBlendsets.Finished") : "blendset-list coppied to clipboard",
		("*", "butl.shapekey.ClearBlendsets") : "clear blendset-list on custom-properties",
		("*", "butl.shapekey.ClearBlendsets.Desc") : "clear blendset-list on custom-properties",
		("*", "butl.shapekey.ClearBlendsets.Finished") : "blendset-list cleared",
		("*", "butl.shapekey.ReflectBlendset") : "selected blendset reflect into shapekey-values",
		("*", "butl.shapekey.ReflectBlendset.Desc") : "selected blendset reflect into shapekey-values",
		("*", "butl.shapekey.ReflectBlendset.Finished") : "blendset(%s) has reflected into shapekey-values.",
		("*", "butl.shapekey.KeyNotFound") : "shapekey(%s) not found.",
		("*", "butl.shapekey.RegistBlendset") : "overwrite to custom-properties from shapekey-values",
		("*", "butl.shapekey.RegistBlendset.Desc") : "overwrite to custom-property from shapekey-values",
		("*", "butl.shapekey.RegistBlendset.Finished") : "Custom-property(%s) overwrited from shapekey-values.",
		("*", "butl.shapekey.AddBlendset") : "add to custom-properties from shapekey-values",
		("*", "butl.shapekey.AddBlendset.Desc") : "add to custom-property from shapekey-values",
		("*", "butl.shapekey.AddBlendset.Finished") : "Custom-property(%s) added from shapekey-values.",
		("*", "butl.shapekey.DelBlendset") : "delete custom-property",
		("*", "butl.shapekey.DelBlendset.Desc") : "delete custom-property",
		("*", "butl.shapekey.DelBlendset.Finished") : "Custom-property(%s) deleted.",
		("*", "butl.shapekey.PasteBlendset") : "paste blendset to shapekey from clipboard",
		("*", "butl.shapekey.PasteBlendset.Desc") : "paste blendset to shapekey from clipboard",
		("*", "butl.shapekey.PasteBlendset.Finished") : "blendset has pasted to shapekey from clipboard",
		("*", "butl.shapekey.CopyBlendset") : "copy blendset to clipboard from shapekey-values",
		("*", "butl.shapekey.CopyBlendset.Desc") : "copy blendset to clipboard from shapekey-values",
		("*", "butl.shapekey.CopyBlendset.Finished") : "shapekey-values has copied to clipboard",
		("*", "butl.shapekey.BsImporterFeature") : "ShapeKey operation feature",
		("*", "butl.shapekey.BsImporterFDesc") : "ShapeKey operation feature",
		("*", "butl.updater.Desc") : "BoneUtil update from GitHub.",
		("*", "butl.updater.Finished") : "Blender-CM3D2-BoneUtil updated(ver:%s). please restart blender.",
		("*", "butl.updater.History") : "Update History",
		("*", "butl.updater.FailedGetHistory") : "failed to get update history",
		("*", "butl.updater.HistoryDays") : "%03d days ago",
		("*", "butl.updater.HistoryHours") :"%02d hours ago",
		("*", "butl.updater.HistoryMins") : "%03d mins ago",
		("*", "butl.updater.HistorySecs") : "%03d secs ago",
		("*", "butl.updater.HistoryUpdated:") : "UpdateTime:",
		("*", "butl.shapekey.CannotOpenFile") : "cannot open file:(%s)",
		("*", "butl.shapekey.Menu.InvalidFile") : "%s is invalid menu file",
		("*", "butl.shapekey.Menu.FailedToParsefile") : "failed to parse menu file(%s)",
		("*", "butl.shapekey.menuif") : "menu I/F",
		("*", "butl.shapekey.Menu.Overwrite") : "Overwrite if filename is empty",
		("*", "butl.shapekey.Menu.ImportfileDesc") : "import menu-file to blendset",
		("*", "butl.shapekey.Menu.BlendsetsImport.Finished") : "blendset(%d) import finished.",
		("*", "butl.shapekey.Menu.ExportfileDesc") : "export to blendset(menu file)",
		("*", "butl.shapekey.Menu.Backup") : "file backup",
		("*", "butl.shapekey.Menu.BackupDesc") : "Duplicate the backup file when overwriting the file",
		("*", "butl.shapekey.Menu.SaveFilename") : "save filename",
		("*", "butl.shapekey.Menu.SaveFilenameDesc") : "overwrite menu file if name is empty.",
		("*", "butl.shapekey.Menu.FailedToParsefile.Export") : "failed to parse menu file (%s) for export",
		("*", "butl.shapekey.Menu.BlendsetsExport.Finished") : "blendset export finished. menu file:%s",
		("*", "butl.shapekey.Menu.BackupExt") : "Extension for backup (Invalid in blanks)",
		("*", "butl.shapekey.Menu.BackupExtDesc") : "use this extension for backup when menu file export. Invalid in blanks",
		("*", "butl.shapekey.Menu.File") : "menu file",
		("*", "butl.shapekey.Menu.InitFolder") : "init folder to select menu file",
		("*", "butl.shapekey.Menu.TargetDir") : "directory for menu file",
		("*", "butl.shapekey.Menu.TargetDirDesc") : "specify folder to select menu file",
		("*", "butl.shapekey.Menu.DefaultPath.Import") : "default path for import menu-file",
		("*", "butl.shapekey.Menu.DefaultPath.ImportDesc") : "default path for import menu-file.",
		("*", "butl.shapekey.Menu.DefaultPath.Export") : "default path for export menu-file",
		("*", "butl.shapekey.Menu.DefaultPath.ExportDesc") : "default path for export menu-file.",
		
		("*", "Select") : "select",
		("*", "selutl.FeatureName") : "Selection Util",
		("*", "selutl.FeatureDesc") : "feature for select vertices/bones",
		("*", "selutl.Key") : "Key",
		("*", "selutl.BasePointB") : "Point B",
		("*", "selutl.Margin") : "margin",
		("*", "selutl.Inclusion") : "inclusion",
		("*", "selutl.Ignorecase") : "ignore case",
		("*", "selutl.SetDefaultMarginDesc") : "set default value to margin",
		("*", "selutl.ClearBaseDesc") : "clear base value",
		("*", "selutl.SymmetryLTB") : "symmetry(< B)",
		("*", "selutl.SymmetryGTB") : "symmetry(> B)",
		("*", "selutl.UpdateSelected") : "vertex selection state updated",
		("*", "selutl.SelPointDesc") : "update vertex selection state",
		("*", "selutl.SelSymmetricPointDesc") : "Select vertices at symmetric positions for the current selected vertex",
		("*", "selutl.SelBoneByNameDesc") : "update bone selection state by name",
		("*", "selutl.SelBoneDesc") : "update bone selection state",
	},
	"ja_JP" : {
		("*", "Import") : "インポート",
		("*", "Export") : "エクスポート",
		("*", "Add") : "追加",
		("*", "Scale") : "スケール(倍率)",
		("*", "Hardness") : "硬さ",
		("*", "BoneType") : "ボーンタイプ",
		
		("*", "butl.AddonDesc") : "カスタムメイド3D2のボーン関連の補助機能を提供します",
		("*", "butl.EnableOption") : "オプション機能 有効化",
		("*", "butl.PushSaveButton") : "ここの設定は「ユーザー設定の保存」ボタンを押すまで保存されていません",
		("*", "butl.BaseBoneName") : "BaseBone名",
		("*", "butl.RenameBone") : "Armature上のBoneリネーム",
		("*", "butl.EnumAll") : "全ボーン",
		("*", "butl.EnumSelected") : "選択ボーンのみ",
		("*", "butl.EnumDescendant") : "選択ボーン+子孫ボーン",
		("*", "butl.Target") : "ターゲット:",
		("*", "butl.ImportTarget:") : "取込み対象:",
		("*", "butl.ScaleDesc") : "modelインポート時の拡大率を指定してください",
		("*", "butl.VertexGroup") : "頂点グループ",
		("*", "butl.VertexGroup:") : "頂点グループ:",
		
		("*", "butl.bdimport.ImportBoneData4CM3D2") : "CM3D2用",
		("*", "butl.bdimport.ImportBoneData") : "BoneData取込み",
		("*", "butl.bdimport.ImportBoneDataDesc") : "Blender上のボーンからCM3D2で使われるBoneDataに変換します",
		("*", "butl.bdimport.RenameBaseBone") : "BaseBoneリネーム",
		("*", "butl.bdimport.RenameBaseBoneDesc") : "カスタムプロパティ上のBaseBoneをリネーム",
		("*", "butl.bdimport.RenameBaseBoneCompleted") : "BaseBoneをリネームしました",
		("*", "butl.bdimport.RemoveBoneDataNonExistent") : "存在しないボーンのBoneData削除",
		("*", "butl.bdimport.ExcludeIKBoneDataForRemove") : "IKボーンは削除しない",
		("*", "butl.bdimport.UseExist") : "既存のみ使用",
		("*", "butl.bdimport.AddVGDesc") : "頂点グループを追加する",
		("*", "butl.bdimport.UseExistDesc") : "既存の頂点グループのみ使用する",
		("*", "butl.bdimport.ImportCompleted") : "BoneData取込み完了",
		("*", "butl.bdimport.ActionMode:") : "動作モード:",
		("*", "butl.bdimport.NormalMode") : "通常動作",
		("*", "butl.bdimport.AutoDetect") : "自動判定",
		("*", "butl.bdimport.OldMode") : "旧版動作",
		("*", "butl.bdimport.NormalModeDesc") : "Converter 0.423 以降のアーマチュアを対象とした取り込み動作",
		("*", "butl.bdimport.AutoDetectDesc") : "自動で旧版かを判定して動作 (判定は完璧ではありません)",
		("*", "butl.bdimport.OldModeDesc") : "Converter 0.414 以前を対象とした取り込み動作",
		("*", "butl.ChangeBoneTypeFeature") : "揺れボーンのタイプ変更",
		("*", "butl.ChangeBoneTypeFDesc") : "揺れボーンのタイプを一括で変更する機能",
		("*", "butl.ChangeBoneType4CM3D2") : "CM3D2用 ボーンタイプ変更",
		("*", "butl.ChangeBoneType") : "ボーンタイプ変更",
		("*", "butl.ChangeBoneTypeCompleted") : "ボーンタイプ変更完了",
		("*", "butl.BoneList") : "揺れボーンリスト",
		("*", "butl.GenMeshFromBoneFeature") : "ボーンからメッシュ作成",
		("*", "butl.GenMeshFromBoneFDesc") : "ボーンからメッシュを作成する機能",
		("*", "butl.GenMeshFromBone") : "ボーンからメッシュ作成",
		("*", "butl.GenMeshFromBoneDesc") : "Blender上のボーンの形に沿ったメッシュを作成します",
		("*", "butl.ObjectName") : "オブジェクト名",
		("*", "butl.Vertices") : "頂点数",
		("*", "butl.VerticesDesc") : "メッシュの基本頂点数を指定してください",
		("*", "butl.Radius") : "メッシュ半径",
		("*", "butl.RadiusDesc") : "メッシュの半径を指定してください",
		("*", "butl.EnumLocalBone") : "LocalBoneのみ",
		("*", "butl.EnumNone") : "フィルタなし",
		("*", "butl.LocalBoneDesc") : "LocalBoneDataにあるボーンのみを対象とする",
		("*", "butl.EnumNoneDesc") : "フィルタなし",
		("*", "butl.CylinderSize:") : "生成メッシュ(円柱)のサイズ",
		("*", "butl.ImportSource:") : "抽出元:",
		("*", "butl.shapekey.BatchOperation") : "シェイプキー一括操作",
		("*", "butl.shapekey.CopySet") : "一括コピー",
		("*", "butl.shapekey.PasteSet"): "一括貼付け",
		("*", "butl.shapekey.ClearSet"): "クリア",
		("*", "butl.shapekey.CopyValue") : "値コピー",
		("*", "butl.shapekey.PasteValue") : "値貼付け",
		("*", "butl.shapekey.BlendsetOpeation") : "Blendset操作",
		("*", "butl.shapekey.BlendsetList") : "Blendsetリスト",
		("*", "butl.shapekey.ShapeKeyVal") : "シェイプキー値",
		("*", "butl.shapekey.Reflect") : "反映",
		("*", "butl.shapekey.Regist") : "上書き",
		("*", "butl.shapekey.PasteBlendsets") : "クリップボードからblendsetの値をカスタムプロパティに貼付け",
		("*", "butl.shapekey.PasteBlendsets.Desc") : "クリップボード内のblendsetの値をカスタムプロパティに設定します",
		("*", "butl.shapekey.PasteBlendsets.Finished") : "クリップボードからblendset情報(%d個)を貼り付けました",
		("*", "butl.shapekey.ParseFailed") : "シェイプキー(%s)の値が数値としてパースできません。スキップします",
		("*", "butl.shapekey.CopyBlendsets") : "カスタムプロパティからクリップボードへコピー",
		("*", "butl.shapekey.CopyBlendsets.Desc") : "カスタムプロパティ上のblendset値をクリップボードへコピーします",
		("*", "butl.shapekey.CopyBlendsets.Finished") : "クリップボードにカスタムプロパティのblendset情報をコピーしました",
		("*", "butl.shapekey.ClearBlendsets") : "カスタムプロパティのblendsetをクリア",
		("*", "butl.shapekey.ClearBlendsets.Desc") : "カスタムプロパティ上のblendsetをクリアします",
		("*", "butl.shapekey.ClearBlendsets.Finished") : "カスタムプロパティのblendset情報をクリアしました",
		("*", "butl.shapekey.ReflectBlendset") : "選択されたBlendsetの値をシェイプキーへ反映",
		("*", "butl.shapekey.ReflectBlendset.Desc") : "選択されたBlendsetの値をシェイプキーへ反映します",
		("*", "butl.shapekey.ReflectBlendset.Finished") : "シェイプキーにblendset(%s)の情報を反映しました",
		("*", "butl.shapekey.KeyNotFound") : "シェイプキー(%s)が存在しないためスキップします",
		("*", "butl.shapekey.RegistBlendset") : "現在のシェイプキー値をBlendsetに上書き",
		("*", "butl.shapekey.RegistBlendset.Desc") : "現在のシェイプキー値をBlendsetに上書きします",
		("*", "butl.shapekey.RegistBlendset.Finished") : "現在のシェイプキー値をカスタムプロパティ(%s)に上書きしました",
		("*", "butl.shapekey.AddBlendset") : "現在のシェイプキー値をBlendsetに追加",
		("*", "butl.shapekey.AddBlendset.Desc") : "現在のシェイプキー値をBlendsetに追加します",
		("*", "butl.shapekey.AddBlendset.Finished") : "現在のシェイプキー値をカスタムプロパティ(%s)に追加しました",
		("*", "butl.shapekey.DelBlendset") : "指定されたBlendsetを削除",
		("*", "butl.shapekey.DelBlendset.Desc") : "指定された名前のBlendsetを削除します",
		("*", "butl.shapekey.DelBlendset.Finished") : "指定されたBlendsetに対応したカスタムプロパティ(%s)に削除しました",
		("*", "butl.shapekey.PasteBlendset") : "クリップボードからblendset値を現在のシェイプキーに貼付け",
		("*", "butl.shapekey.PasteBlendset.Desc") : "クリップボードからblendset値を現在のシェイプキーに貼付けます",
		("*", "butl.shapekey.PasteBlendset.Finished") : "blendset情報を貼り付けました",
		("*", "butl.shapekey.CopyBlendset") : "現在のシェイプキーの値をクリップボードへコピー",
		("*", "butl.shapekey.CopyBlendset.Desc") : "現在のシェイプキーの値をクリップボードへコピーします",
		("*", "butl.shapekey.CopyBlendset.Finished") : "クリップボードにシェイプキーの値をコピーしました",
		("*", "butl.shapekey.BsImporterFeature") : "シェイプキー値変更機能",
		("*", "butl.shapekey.BsImporterFDesc") : "シェイプキー値の変更機能",
		("*", "butl.updater.Desc") : "GitHubから最新版のBoneUtilアドオンをダウンロードし上書き更新します",
		("*", "butl.updater.Finished") : "Blender-CM3D2-BoneUtilを更新(ver:%s)しました。Blenderを再起動してください",
		("*", "butl.updater.History") : "CM3D2 BoneUtilの更新履歴",
		("*", "butl.updater.FailedGetHistory") : "更新履歴の取得に失敗しました",
		("*", "butl.updater.HistoryDays")  : "%04d日前",
		("*", "butl.updater.HistoryHours") : "%02d時間前",
		("*", "butl.updater.HistoryMins")  : " %03d分前",
		("*", "butl.updater.HistorySecs")  : " %03d秒前",
		("*", "butl.updater.HistoryUpdated:") : "履歴取得時刻：",
		("*", "butl.shapekey.CannotOpenFile") : "ファイル(%s)を開けません (ファイルが見つからない、アクセス権限がない等)",
		("*", "butl.shapekey.Menu.InvalidFile") : "%sはmenuファイルではありません. 処理を中断します",
		("*", "butl.shapekey.Menu.FailedToParsefile") : "menuファイル(%s)の取り込み中に問題が発生しました",
		("*", "butl.shapekey.menuif") : ".menu 連携",
		("*", "butl.shapekey.Menu.Overwrite") : "↑ファイル名を指定しない場合は上書き",
		("*", "butl.shapekey.Menu.ImportfileDesc") : "menuファイルからblendsetを取り込みます",
		("*", "butl.shapekey.Menu.BlendsetsImport.Finished") : "menuからblendset情報(%d個)を取り込みました",
		("*", "butl.shapekey.Menu.ExportfileDesc") : "指定されたmenuファイルをベースにblendsetを出力します",
		("*", "butl.shapekey.Menu.Backup") : "ファイルをバックアップ",
		("*", "butl.shapekey.Menu.BackupDesc") : "ファイルに上書きする場合にバックアップファイルを複製します",
		("*", "butl.shapekey.Menu.SaveFilename") : "保存ファイル名",
		("*", "butl.shapekey.Menu.SaveFilenameDesc") : "未指定の場合は、ベースとなるmenuファイルを上書きします",
		("*", "butl.shapekey.Menu.FailedToParsefile.Export") : "エクスポート処理のベースとするmenuファイル(%s)の読み込み中に問題が発生しました",
		("*", "butl.shapekey.Menu.BlendsetsExport.Finished") : "blendset情報をmenuファイルに出力しました:%s",
		("*", "butl.shapekey.Menu.BackupExt") : "バックアップの拡張子 (空欄で無効)",
		("*", "butl.shapekey.Menu.BackupExtDesc") : "エクスポート時にバックアップをこの拡張子で作成します、空欄でバックアップを無効",
		("*", "butl.shapekey.Menu.File") : "menuファイル",
		("*", "butl.shapekey.Menu.InitFolder") : "menuファイル選択の初期フォルダ",
		("*", "butl.shapekey.Menu.TargetDir") : "menuファイル配置ディレクトリ",
		("*", "butl.shapekey.Menu.TargetDirDesc") : "設定すれば、menuを扱う時は必ずここからファイル選択を始めます",
		("*", "butl.shapekey.Menu.DefaultPath.Import") : "menuインポート時のデフォルトパス",
		("*", "butl.shapekey.Menu.DefaultPath.ImportDesc") : "menuインポート時に最初はこのパスが表示されます、インポート毎に保存されます",
		("*", "butl.shapekey.Menu.DefaultPath.Export") : "menuエクスポート時のデフォルトパス",
		("*", "butl.shapekey.Menu.DefaultPath.ExportDesc") : "menuエクスポート時に最初はこのパスが表示されます、エクスポート毎に保存されます",
	
		("*", "Select") : "選択",
		("*", "selutl.FeatureName") : "選択支援機能",
		("*", "selutl.FeatureDesc") : "頂点・ボーンの選択を支援する機能",
		("*", "selutl.Key") : "キー",
		("*", "selutl.BasePointB") : "基準点B",
		("*", "selutl.Margin") : "マージン",
		("*", "selutl.Inclusion") : "包含",
		("*", "selutl.Ignorecase") : "大文字小文字の区別無し",
		("*", "selutl.SetDefaultMarginDesc") : "マージン値にデフォルト値を設定",
		("*", "selutl.SymmetryLTB") : "対称位置(< B)",
		("*", "selutl.SymmetryGTB") : "対称位置(> B)",
		("*", "selutl.UpdateSelected") : "選択状態を更新しました。",
		("*", "selutl.UpdateSelectedBones") : "ボーンの選択状態を更新しました。",
		("*", "selutl.SelPointDesc") : "条件に合った頂点を選択する",
		("*", "selutl.SelSymmetricPointDesc") : "現在の選択頂点に対して、対称位置の頂点を選択する",
		("*", "selutl.SelBoneByNameDesc") : "キーワードでボーンの選択状態を更新する",
		("*", "selutl.SelBoneDesc") : "ボーンの選択状態を更新する",
	}
}
