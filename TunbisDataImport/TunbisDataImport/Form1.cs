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
           

            // Excel dosyas�n� a�
            using (var package = new ExcelPackage(new FileInfo("@\"C:\\data.xls\"")))
            {
                // �lk sayfay� al (0-tabanl�)
                var worksheet = package.Workbook.Worksheets[0];

                // Verileri saklamak i�in bir liste olu�tur
                List<Dictionary<string, object>> data = new List<Dictionary<string, object>>();

                // Excel sayfas�ndaki verileri oku ve JSON verisi olu�tur
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

                // JSON'a d�n��t�r
                string jsonData = Newtonsoft.Json.JsonConvert.SerializeObject(data, Newtonsoft.Json.Formatting.Indented);

                // JSON verisini kullanmak i�in jsonData de�i�kenini kullanabilirsiniz.
            }

        }
    }
}