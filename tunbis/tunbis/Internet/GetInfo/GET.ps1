
# Excel uygulamasını oluştur
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $true
$workbook = $excel.Workbooks.Add()
$worksheet = $workbook.Worksheets.Item(1)
$worksheet.Name = "Computer Information"

$output_path = "D:"
$output_path_network = "\\162.162.5.2\GetInfo"

# Başlık satırını yaz
$headerRow = 1
$columns = "A", "B", "C", "D", "E", "F", "G", "H", "I" ,"J" , "K", "M", "N", "O", "P", "Q", "R", "S", "T" ,"U" , "V", "W", "X", "Y", "Z", "AA", "AB", "AC","AD","AF","AG","AH","AI","AJ"
$headers = "Computer Name", "Manufacturer", "Model", "Number of Processors", "System Type", "Serial Number", "Processor Name", "Number of Cores", "Max Clock Speed (GHz)", "Graphics Card", "BIOS Version", "Product", "Base Board Serial Number", "Number of Memory Slots", "Total RAM (GB)", "Used RAM Slots", "IP Address", "Disk Drive Model", "Disk Size (GB)", "Media Type", "Disk Partition Name", "Operating System", "OS Version", "OS Build Number", "Office Version", "Office License Status", "Disk Usage (%)", "RAM Brands","Average RAM Speed","RAM Slot Types"

for ($i = 0; $i -lt $columns.Length; $i++) {
    $cell = $worksheet.Cells.Item($headerRow, $i + 1)
    $cell.Value2 = $headers[$i]
}

# Bilgisayar özelliklerini alma
$computerName = $env:COMPUTERNAME
$computerSystem = Get-WmiObject Win32_ComputerSystem
$processor = Get-WmiObject Win32_Processor
$videoController = Get-WmiObject Win32_VideoController
$BIOS = Get-WmiObject Win32_BIOS
$BaseBoard = Get-WmiObject Win32_BaseBoard
$physicalMemory = Get-WmiObject Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum
$networkAdapter = Get-WmiObject Win32_NetworkAdapterConfiguration | Where { $_.IPAddress -ne $null -and $_.IPEnabled }
$diskDrive = Get-WmiObject Win32_DiskDrive
$diskPartition = Get-WmiObject Win32_DiskPartition
$operatingSystem = Get-WmiObject Win32_OperatingSystem
$officeInfo = Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "Microsoft Office*"}
$ramBrands = (Get-WmiObject Win32_PhysicalMemory | Select-Object -ExpandProperty Manufacturer -Unique) -join ","
$ramSpeeds = Get-WmiObject Win32_PhysicalMemory | Select-Object -ExpandProperty Speed
$averageRamSpeed = ($ramSpeeds | Measure-Object -Average).Average
$ramSlots = Get-WmiObject Win32_PhysicalMemory | Select-Object -ExpandProperty MemoryType
$uniqueRamSlots = $ramSlots | Sort-Object -Unique
$ramSlotTypes = $uniqueRamSlots -join ","

# Disk doluluk oranını al
$disk = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'" | Select-Object -ExpandProperty FreeSpace
$totalDiskSpace = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'" | Select-Object -ExpandProperty Size
$usedDiskSpace = $totalDiskSpace - $disk
$diskUsagePercentage = [math]::Round(($usedDiskSpace / $totalDiskSpace) * 100, 2)

# Bilgisayar özelliklerini Excel tablosuna yazma
$row = $headerRow + 1
$worksheet.Cells.Item($row, 1) = $computerName
$worksheet.Cells.Item($row, 2) = $computerSystem.Manufacturer
$worksheet.Cells.Item($row, 3) = $computerSystem.Model
$worksheet.Cells.Item($row, 4) = $computerSystem.NumberOfProcessors
$worksheet.Cells.Item($row, 5) = $computerSystem.SystemType
$worksheet.Cells.Item($row, 6) = $BIOS.SerialNumber
$worksheet.Cells.Item($row, 7) = $processor.Name
$worksheet.Cells.Item($row, 8) = $processor.NumberOfCores
$worksheet.Cells.Item($row, 9) = [math]::Round($processor.MaxClockSpeed / 1e9, 2)
$worksheet.Cells.Item($row, 10) = $videoController.Name
$worksheet.Cells.Item($row, 11) = $BIOS.SMBIOSBIOSVersion
$worksheet.Cells.Item($row, 12) = $baseBoard.Product
$worksheet.Cells.Item($row, 13) = $baseBoard.SerialNumber
$worksheet.Cells.Item($row, 14) = $baseBoard.NumberOfMemorySlots
$worksheet.Cells.Item($row, 15) = [math]::Round($physicalMemory.Sum / 1GB, 2)
$worksheet.Cells.Item($row, 16) = $physicalMemory.Count
$worksheet.Cells.Item($row, 17) = $networkAdapter.IPAddress
$worksheet.Cells.Item($row, 18) = $diskDrive.Model
$worksheet.Cells.Item($row, 19) = [math]::Round($diskDrive.Size / 1GB, 2)
$worksheet.Cells.Item($row, 20) = if ($diskDrive.MediaType -like "*Fixed*") { "SSD" } else { "HDD" }
$worksheet.Cells.Item($row, 21) = $diskPartition.Name
$worksheet.Cells.Item($row, 22) = $operatingSystem.Caption
$worksheet.Cells.Item($row, 23) = $operatingSystem.Version
$worksheet.Cells.Item($row, 24) = $operatingSystem.BuildNumber
$worksheet.Cells.Item($row, 25) = $officeInfo.Version
$worksheet.Cells.Item($row, 26) = $officeInfo.InstallDate
$worksheet.Cells.Item($row, 27) = $diskUsagePercentage
$worksheet.Cells.Item($row, 28) = $ramBrands
$worksheet.Cells.Item($row, 29) = $averageRamSpeed
$worksheet.Cells.Item($row, 30) = $ramSlotTypes

# Excel dosyasını kaydet
$excelFilePath = "\\162.162.5.2\GetInfo\$computerName.xlsx"
$workbook.SaveAs($excelFilePath)
$workbook.Close()
$excel.Quit()

# Excel nesnelerini serbest bırak
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($worksheet) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
Remove-Variable excel, workbook, worksheet
