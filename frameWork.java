import java.util.*;
import java.sql.*;
import java.io.*;

class CRUD {
    private Connection connection;
    private Statement stmt;
    private PreparedStatement pstmt;
    private ResultSet rs;
    private String tableName;
    private List<String> fields;
    private String menu;
    private Scanner sc = new Scanner(System.in);

    CRUD() {
        getConnection();
        tableName = "Customer";
        getFields(tableName);
        menu = getMenu();
        showMenu(menu);
    }

    public void showMenu(String menu) {
        while (true) {
            printMenu(menu);
            System.out.print("Enter Your Choice: ");
            int choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                 create();
                 break;
                case 2:
                 showAll();
                 break;
                case 3:
                 update();
                 break;
                case 4:
                 delete();
                 break;
                case 5: 
                    System.out.println("Exiting...");
                    closeConnection();
                    System.exit(0);
                
                default:
                 System.out.println("Please enter a valid choice!");
                 break;
            }
        }
    }

    public void printMenu(String menu) {
        System.out.println(menu);
    }

    void create() {
    		List<String> values = new ArrayList<>();
    		values = readRecord();
    		saveRecordInDatabase(values);
            System.out.println("Record added successfully!");
    }
    void saveRecordInDatabase(List<String> values)
    {
    	try {
            String placeholders = String.join(",", Collections.nCopies(fields.size(), "?"));
            String query = "INSERT INTO " + tableName + " VALUES (" + placeholders + ")";
            pstmt = connection.prepareStatement(query);

            for (int counter = 0; counter < values.size(); counter++) {
                pstmt.setString(counter + 1, values.get(counter));
            }
            pstmt.executeUpdate();
        }
        catch (SQLException e)
        {
        	System.out.println(e);
        }
     }
    List<String> readRecord()
    {
        try {
            List<String> values = new ArrayList<>();

            for (String field : fields) {
                System.out.print("Enter " + field + ": ");
                values.add(sc.nextLine());
            }
            return values;
        }
      	 catch (Exception e) {
            System.out.println("Error adding record: " + e.getMessage());
        }
        return null;
    }

    void showAll() {
        try {
            System.out.println("\n--- All Records ---");
            stmt = connection.createStatement();
            rs = stmt.executeQuery("SELECT * FROM " + tableName);

            while (rs.next()) {
            	printRecord(rs);
                System.out.println();
            }
        } catch (SQLException e) {
            System.out.println("Error showing records: " + e.getMessage());
        }
    }
    void printRecord(ResultSet rs)
    {
    	try {
        for (int counter = 0; counter < fields.size(); counter++) {
            System.out.println(fields.get(counter) + ": " + rs.getString(counter + 1));
        }
    }
    catch (Exception e)
    {
    	System.out.println(e);
    }
	}
    void update() {
        System.out.println("Update");
    }

    void delete() {
        System.out.println("Delete");
    }

    void getFields(String tableName) {
        this.fields = new ArrayList<>();
        try {
            stmt = connection.createStatement();
            rs = stmt.executeQuery("DESCRIBE " + tableName);
            while (rs.next()) {
                fields.add(rs.getString(1));
            }
            System.out.println("Fields found: " + fields);
        } catch (SQLException e) {
            System.out.println("Error fetching fields: " + e.getMessage());
        }
    }

    static String getMenu() {
        String fileName = "menu.properties";
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            StringBuilder menuContent = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null)
                menuContent.append(line).append("\n");
            return menuContent.toString();
        } catch (IOException e) {
            return null;
        }
    }

    Connection getConnection() {
        try {
            connection = DriverManager.getConnection(
                "jdbc:mysql://138.68.140.83:3306/HariDmart",
                "Hari",
                "Hari@123"
            );
            System.out.println("Connected to MySQL...");
        } catch (SQLException e) {
            System.out.println("Could not connect to Database: " + e.getMessage());
        }
        return connection;
    }

    void closeConnection() {
        try {
            if (connection != null)
                connection.close();
        } catch (SQLException e) {
            System.out.println("Error closing connection!");
        }
    }
}

class cMain {
    public static void main(String[] args) {
        CRUD object = new CRUD();
    }
}
