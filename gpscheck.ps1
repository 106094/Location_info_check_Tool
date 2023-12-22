
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force;
Add-Type -AssemblyName System.Windows.Forms

$mainpath=read-host "請將csv檔案拖曳至此"

$mainfilepath=$mainpath.replace("""","")

if(!(test-path $mainfilepath)){
[System.Windows.Forms.MessageBox]::Show($this,"fail is no found, please check")   
exit
}

$mainfile=Split-Path -Leaf $mainfilepath
$mainpath=(Split-Path $mainfilepath)+"\"
$mainfilenew=$mainfile.replace(".csv","_new.csv")
$mainfilepathnew=$mainpath+$mainfilenew

$csvraw=get-content $mainfilepath

$filmap="\\192.168.20.20\sto\EO\2_AutoTool\ALL\148.AppleCarPlay_Location_info_check_Tool\failmapping.csv"
if(!(test-path $filmap)){
  $filmap="$PSScriptRoot\failmapping.csv"
}

if(!(test-path $filmap)){
[System.Windows.Forms.MessageBox]::Show($this,"no failmapping.csv file is found, please check")   
exit
}



#$mainfilepath
#$mainfile
#$mainfilenew
#$mainfilepathnew

$totaladdcol=32
$addclo=1
$newline=$null
while($addclo -le $totaladdcol){
if($addclo -gt 26){
$addclo2=$addclo-26
$newline+="A"+@([CHAR](64+$addclo2))
}else{
$newline+=@([CHAR](64+$addclo))
}
$addclo++
}

$transcount=1
$addclo=1
while($addclo -le $transcount){
$newline+=@("trans"+$addclo)
$addclo++
}


$failcount=7
$addclo=1
while($addclo -le $failcount){
$newline+=@("fail"+$addclo)
$addclo++
}


$newlinetitle=$newline -join ","

$csvrawnew=$csvraw|ForEach-Object{

if($csvraw.indexof($_) -eq 0){
$_=$newlinetitle
}
$_=$_.replace("""","")
$_
}

$csvrawnew|out-file $mainfilepathnew

$csvcontent=import-csv $mainfilepathnew

#region criteria

<#
資料剖析
確認是否有PASCD, GPGGA, GPRMC
將三種GPS型式分開來

#>
#endregion

$mapcontent=import-csv $filmap -Encoding UTF8

$GPS_info=@("GPGGA","GPRMC","PASCD")
foreach($GPS_inf in $GPS_info){
  
 $gpsfail180=$null
 $gpgga_suffix=$null
 $fail_map=$mapcontent|Where-Object{$_.gpstype -match $GPS_inf}

 $content_gp_fail=$null
 $passflag=$true

 $gpscontent=$csvcontent|?{$_.B -match "$GPS_inf" }

 $gpsfilename=$mainfile.replace(".csv","_$($GPS_inf).csv")
 
 $filepath=$mainpath+$gpsfilename

 $gpscontent|export-csv -path  $filepath -NoTypeInformation
 $content_gps=import-csv $filepath

#region "GPGGA"

 <#
GPGGA
1. 全部欄位不能有空白 - fail1
2. D欄, F欄 - 經緯度確認到小數點四位  - fail2
3. H欄 - GPS狀態不可顯示為0 - fail3
4. L欄, M欄 - 海拔高度單位需顯示為M - fail4
5. E欄 - 緯度半球必須為N - fail5
6. G欄 - 經度半球必須為E - fail6
7. H欄 - 不能全部為6 或 6連續超過500次 - fail7
#>

  if($GPS_inf -eq "GPGGA"){
 
  foreach($content_gp in $content_gps){

   $failno="fail1"
   $cols=($fail_map|Where-Object{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|ForEach-Object{
  if(($content_gp.$_).length -eq 0){
  $content_gp.$failno=$content_gp.$_
    } 
  }

   $failno="fail2"
   $cols=($fail_map|Where-Object{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|ForEach-Object{

   $valuedata=(($content_gp.$_).split("."))[1]
     
  try{$valuedata.substring(3,1)|Out-Null}catch{
    $content_gp.$failno=$content_gp.$_
  } 
  }

  
   $failno="fail3"
   $cols=($fail_map|Where-Object{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|ForEach-Object{
    if($content_gp.$_ -eq 0){
    $content_gp.$failno=$content_gp.$_
  }
  }

   $failno="fail4"
   $cols=($fail_map|Where-Object{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

 $colall|ForEach-Object{

  if(($content_gp.$_) -ne "M"){
  $lineher=$content_gp
   $testhere=$content_gp.$_
    $content_gp.$failno=$content_gp.$_
   
  } 
  }

  
   $failno="fail5"
   $cols=($fail_map|Where-Object{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

 $colall|ForEach-Object{
  if(($content_gp.$_) -ne "N"){
    $content_gp.$failno=$content_gp.$_
  } 
 }

 
   $failno="fail6"
   $cols=($fail_map|Where-Object{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

 $colall|ForEach-Object{
  if(($content_gp.$_) -ne "E"){
    $content_gp.$failno=$content_gp.$_
  } 
  }
 }

    $failno="fail7"
    $cols=($fail_map|Where-Object{$_.failno -eq $failno}).column
    $colall=$cols.ToCharArray()
    ForEach($colall1 in $colall){
      $indexnums=$content_gps.$colall1
      $i=0
      
      ForEach ($indexnum in $indexnums){
          if($indexnum -eq 6){
            $i++
          }
          else{
            $i=0
          }

      }
      if($i -eq $indexnums.count){
       $gpgga_suffix+="_all_H_is6"
      }
      if($i -gt 500){
        $gpgga_suffix+="_H_is6_ove500"
       }
    }


   $content_gps|export-csv -path  $filepath -NoTypeInformation 
  $content_gp_fail= $content_gps|?{($_.fail1).length -gt 0 -or ($_.fail2).length -gt 0 -or ($_.fail3).length -gt 0 -or ($_.fail4).length -gt 0 -or ($_.fail5).length -gt 0 -or ($_.fail6).length -gt 0}
  }

  #endregion

#region "GPRMC"

 <#
GPRMC
1. 全部欄位不能有空白 - fail1
2. D欄 - 定位狀態不能為V - fail2
3. E欄, G欄 - 經緯度確認到小數點四位 - fail3
4. I欄 - 地面速度單位是節，可以的話請幫忙換算成時速在後面空白欄位 (I欄數值*1.852) - trans1
5. J欄 - 地面航向最大值與最小值要相差180度以上   - fail4 add to 檔名
6. N欄 - 模式指示不應為N開頭  - fail5
7. F欄 - 緯度半球必須為N - fail6
8. H欄 - 經度半球必須為E - fail7

#>

  if($GPS_inf -eq "GPRMC"){
  
 $maxang= ($gpscontent.J|measure -Maximum).Maximum
 $minang= ($gpscontent.J|measure -Minimum).Minimum
 $anggap=$maxang - $minang
     
   if( $anggap -lt "180" ){
    
    $gpsfail180="_less180_$($maxang)_$($minang)"

    #$gpsfilename_fail=$mainfile.replace(".csv","_$($GPS_inf)_fail_less180_$($maxang)_$($minang).csv")

  }

  foreach($content_gp in $content_gps){
   
   $failno="fail1"
   $cols=($fail_map|?{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|%{

  if(($content_gp.$_).length -eq 0){
  $content_gp.$failno=$content_gp.$_
  } 
  }
  
  
   $failno="fail2"
   $cols=($fail_map|?{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|%{

  if( $content_gp.$_ -eq "V"){
   $content_gp.$failno=$content_gp.$_
  }
  }

  
   $failno="fail3"
   $cols=($fail_map|?{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|%{
   $valuedata=(($content_gp.$_).split("."))[1]   
  try{$valuedata.substring(3,1)|out-null}catch{
    $content_gp.$failno=$content_gp.$_|out-string
  } 
  }
   
   $failno="trans1"
   $cols=($fail_map|?{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()
   $colall|%{
    $content_gp.$failno=[double]($content_gp.$_) * 1.852
    }


    
   $failno="fail5"
   $cols=($fail_map|?{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|%{

  $checkN=($content_gp.$_).Substring(0,1)
  if( $checkN -eq "N"){
     $content_gp.$failno=$content_gp.$_
  }
  }

     $failno="fail6"
   $cols=($fail_map|?{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|%{

    if( $content_gp.$_ -ne "N"){
   $content_gp.$failno=$content_gp.$_
    }
   }  

  
   $failno="fail7"
   $cols=($fail_map|?{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()


  $colall|%{
   if( $content_gp.$_ -ne "E"){
   $content_gp.$failno=$content_gp.$_
    }
    }

 }

    $content_gps|export-csv -path  $filepath -NoTypeInformation 
    $content_gp_fail= $content_gps|?{($_.fail1).length -gt 0 -or ($_.fail2).length -gt 0 -or ($_.fail3).length -gt 0 -or ($_.fail4).length -gt 0 -or ($_.fail5).length -gt 0 -or ($_.fail6).length -gt 0 -or ($_.fail7).length -gt 0}
    
 }

  #endregion

  #region "PASCD"

 <#

PASCD
1. 全部欄位不能有空白 - fail1
2. D欄 - Sensor Type ，此欄只能顯示為C - fail2
3. E欄 - 檔位狀態，不能顯示為 - fail3
4. I欄 - 速度表示為公尺/秒，可以的話請幫忙換算成時速在後面空白欄位(I欄數值*3.6) - trans1
   但此欄會與檢查碼一起出現，可能需要在對I欄做一次資料剖析將檢查碼拿掉。


#>

  if($GPS_inf -eq "PASCD"){
 

  foreach($content_gp in $content_gps){

  
   $failno="fail1"
   $cols=($fail_map|?{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|%{

  if(($content_gp.$_).length -eq 0){
   $content_gp.$failno=$content_gp.$_
  } 
  }
  
  
   $failno="fail2"
   $cols=($fail_map|?{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|%{

  if( $content_gp.$_ -ne "C"){
   $content_gp.$failno=$content_gp.$_
  }
  }
  
  
   $failno="fail3"
   $cols=($fail_map|?{$_.failno -eq $failno}).column
   $colall=$cols.ToCharArray()

  $colall|%{
    if( $content_gp.$_ -eq "U"){
    $content_gp.$failno=$content_gp.$_
  }
  }

  $content_gp.trans1=[double]((($content_gp.I).split("*"))[0])*3.6

  
 }

  $content_gps|export-csv -path  $filepath -NoTypeInformation 

 $content_gp_fail= $content_gps|?{($_.fail1).length -gt 0 -or ($_.fail2).length -gt 0 -or ($_.fail3).length -gt 0 }



 }

  #endregion
  
  
  

  
  if((($content_gp_fail).A).count -gt 0){
   $failflag="fail"
  }
   
   if($gpsfail180.lengh -gt 0){
    $failflag=$failflag+$gpsfail180
   #$gpsfilename_fail=$mainfile.replace(".csv","_$($GPS_inf)_fail_less180_$($maxang)_$($minang).csv")
   }

   if($gpgga_suffix.length -gt 0){
    $failflag=$failflag+$gpgga_suffix
   }

    $failflag= ($failflag|Out-String).Trim()
        
 $gpsfilename_fail=$mainfile.replace(".csv","_$($GPS_inf)_$($failflag).csv")
 $gpsfilename_pass=$mainfile.replace(".csv","_$($GPS_inf)_pass.csv")

 $filepath_fail=$mainpath+$gpsfilename_fail
  $filepath_pass=$mainpath+$gpsfilename_pass

if((($content_gp_fail).A).count -gt 0 -or $gpsfail180.length -gt 0 -or $gpgga_suffix.length -gt 0 ){
$filepathcsv=$filepath_fail
 $content_gp_fail | export-csv -path   $filepath_fail -NoTypeInformation
  }
  else{
  $filepathcsv=$filepath_pass
  move-item  $filepath  $filepath_pass -Force
  }

 #revise headers

$data = get-content -Path  $filepathcsv
$newdata=$data|%{
$newline=$_
if($data.indexof($_) -eq 0){
foreach($fail_map1 in $fail_map){
$failnoname=$fail_map1.failno
$failitem=$fail_map1.failitem
$newline=$newline -replace $failnoname,$failitem
}
}
$newline
}
$newdata|set-content $filepathcsv -Encoding UTF8


}


$csvcontent|export-csv $mainfilepathnew -NoTypeInformation
#remove-item $mainfilepathnew -Force 

[System.Windows.Forms.MessageBox]::Show($this,"Location Data Check Complete!") 