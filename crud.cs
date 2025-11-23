// CRUD program using MySQL

using System;
using System.IO;
using System.Data;
using MySql.Data.MySqlClient;
using System.Collections.Generic;

class CRUD
{
    MySqlConnection connection;
    string tableName = "Cashier";
    string menu;
    List<string> fields = new List<string>();

    public CRUD()
    {
        getConnection();
        LoadColumns();  
        menu = GetMenu();
        ShowMenu();
    }

    void getConnection()
    {
        string connectionString = "server=138.68.140.83;user=Hari;password=Hari@123;database=HariDmart;";

        try
        {
            connection = new MySqlConnection(connectionString);
            connection.Open();
        }
        catch (MySqlException e)
        {
            Console.WriteLine("Database connection failed: " + e.Message);
        }
    }

    void LoadColumns()
    {
        string sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS " +
                     "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = @table";

        MySqlCommand cmd = new MySqlCommand(sql, connection);
        cmd.Parameters.AddWithValue("@table", tableName);

        MySqlDataReader reader = cmd.ExecuteReader();

        while (reader.Read())
        {
            fields.Add(reader.GetString(0));
        }
        reader.Close();
    }

    void Create()
    {
        List<string> values = ReadRecord();

        string columns = string.Join(", ", fields);
        string placeholders = string.Join(", ", fields.ConvertAll(f => "@" + f));

        string sql = "INSERT INTO " + tableName +
                     " (" + columns + ") VALUES (" + placeholders + ")";

        try
        {
            MySqlCommand command = new MySqlCommand(sql, connection);

            for (int i = 0; i < fields.Count; i++)
            {
                command.Parameters.AddWithValue("@" + fields[i], values[i]);
            }

            int rows = command.ExecuteNonQuery();

            Console.WriteLine(rows > 0 ? "Record inserted successfully.\n"
                                       : "No record inserted.\n");
        }
        catch (MySqlException e)
        {
            Console.WriteLine("SQL Error: " + e.Message);
        }
    }

    List<string> ReadRecord()
    {
        List<string> values = new List<string>();

        foreach (var field in fields)
        {
            Console.Write("Enter " + field + ": ");
            values.Add(Console.ReadLine());
        }
        return values;
    }

    void ShowAll()
    {
        string sql = "SELECT * FROM " + tableName;

        //using data reader
        // MySqlCommand cmd = new MySqlCommand(sql, connection);
        // MySqlDataReader reader = cmd.ExecuteReader();

        // Console.WriteLine("\n---- All Records ----");

        // while (reader.Read())
        // {
        //     for (int i = 0; i < reader.FieldCount; i++)
        //     {
        //         Console.Write(reader.GetValue(i) + "\t");
        //     }
        //     Console.WriteLine();
        // }

        // reader.Close();
        // Console.WriteLine();

        //using datatable
        MySqlCommand cmd = new MySqlCommand(sql, connection);
        MySqlDataAdapter adapter = new MySqlDataAdapter(cmd);
        DataTable table = new DataTable();

        // //using data set
        // DataSet ds = new DataSet();
        // adapter.Fill(ds);
        // DataTable table = ds.Tables[0];

        adapter.Fill(table);

        Console.WriteLine("\n---- All Records ----");

        foreach (DataRow row in table.Rows)
        {
            foreach (var item in row.ItemArray)
            {
                Console.Write(item + "\t");
            }
            Console.WriteLine();
        }
    }

    void Update()
    {
        string primaryKey = fields[0];

        Console.Write("Enter " + primaryKey + " to update: ");
        string id = Console.ReadLine();

        List<string> updateValues = new List<string>();

        for (int i = 1; i < fields.Count; i++)
        {
            Console.Write("Enter new " + fields[i] + ": ");
            updateValues.Add(Console.ReadLine());
        }

        string setPart = "";
        for (int i = 1; i < fields.Count; i++)
        {
            setPart += fields[i] + " = @" + fields[i];
            if (i < fields.Count - 1)
                setPart += ", ";
        }

        string sql = "UPDATE " + tableName +
                     " SET " + setPart +
                     " WHERE " + primaryKey + "=@id";

        MySqlCommand cmd = new MySqlCommand(sql, connection);
        cmd.Parameters.AddWithValue("@id", id);

        for (int i = 1; i < fields.Count; i++)
        {
            cmd.Parameters.AddWithValue("@" + fields[i], updateValues[i - 1]);
        }

        int rows = cmd.ExecuteNonQuery();

        Console.WriteLine(rows > 0 ? "Record updated.\n"
                                   : "Record not found.\n");
    }

    void Delete()
    {
        string primaryKey = fields[0];

        Console.Write("Enter " + primaryKey + " to delete: ");
        string id = Console.ReadLine();

        string sql = "DELETE FROM " + tableName +
                     " WHERE " + primaryKey + "=@id";

        MySqlCommand cmd = new MySqlCommand(sql, connection);
        cmd.Parameters.AddWithValue("@id", id);

        int rows = cmd.ExecuteNonQuery();

        Console.WriteLine(rows > 0 ? "Record deleted.\n"
                                   : "Record not found.\n");
    }

    void ShowMenu()
    {
        while (true)
        {
            PrintMenu();
            int choice = Convert.ToInt32(Console.ReadLine());

            switch (choice)
            {
                case 1: Create(); break;
                case 2: ShowAll(); break;
                case 3: Update(); break;
                case 4: Delete(); break;
                case 5: Environment.Exit(0); break;
                default:
                    Console.WriteLine("Invalid choice.\n");
                    break;
            }
        }
    }

    void PrintMenu()
    {
        Console.WriteLine(menu ?? "Menu file not found.");
    }

    string GetMenu()
    {
        string fileName = "menu.cfg";
        try { return File.ReadAllText(fileName); }
        catch { return null; }
    }

    public static void Main(string[] args)
    {
        CRUD crudObj = new CRUD();
    }
}
