using OfficeOpenXml;

namespace TunbisDataImport
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
           

            // Excel dosyasýný aç
            using (var package = new ExcelPackage(new FileInfo("@\"C:\\data.xls\"")))
            {
                // Ýlk sayfayý al (0-tabanlý)
                var worksheet = package.Workbook.Worksheets[0];

                // Verileri saklamak için bir liste oluþtur
                List<Dictionary<string, object>> data = new List<Dictionary<string, object>>();

                // Excel sayfasýndaki verileri oku ve JSON verisi oluþtur
                for (int row = 2; row <= worksheet.Dimension.Rows; row++)
                {
                    Dictionary<string, object> rowData = new Dictionary<string, object>();
                    for (int col = 1; col <= worksheet.Dimension.Columns; col++)
                    {
                        string header = worksheet.Cells[1, col].Value.ToString();
                        object cellValue = worksheet.Cells[row, col].Value;
                        rowData[header] = cellValue;
                    }
                    data.Add(rowData);
                }

                // JSON'a dönüþtür
                string jsonData = Newtonsoft.Json.JsonConvert.SerializeObject(data, Newtonsoft.Json.Formatting.Indented);

                // JSON verisini kullanmak için jsonData deðiþkenini kullanabilirsiniz.
            }

        }
    }
}