<?php

$websockserver = "192.168.1.68";
$websockport = "9000";

// Dont edit anything below here unless you know what your doing!

class MyDB extends SQLite3
{
    function __construct()
    {
        $this->open('/etc/homeremote/database.db');
    }
    function select($query) {
        $result = $this->query($query);
        return $result->fetchArray();
    }
    function insert($query) {
        $this->exec($query);
    }
    function update($query) {
        $this->exec($query);
    }
}


$sDatabaseFileName = '/etc/homeremote/database.db';
$GLOBALS['db'] = new SQlite3ToJSONConverter($sDatabaseFileName);

/**
 * The aim of this class is to offer a transformation
 * of a SQLite database to its JSON stirng format equivalent
 * @author Samuel Grau : <samuel.grau@gmail.com>
 */
class SQlite3ToJSONConverter {
    //==========================================================================
    // Private properties
    //==========================================================================

    /**
     * The SQlite 3 database
     */
    private $database = NULL;

    //==========================================================================
    // Constructors / Destructors
    //==========================================================================

    /**
     * Open the database by creating a new SQLite3 instance from the
     * filename given to the constructor initially
     */
    public function __construct($sDatabaseFileName = NULL) {
        $this->openDatabase($sDatabaseFileName);
    }

    //==========================================================================
    // Protected methods
    //==========================================================================

    /**
     * Open the database by creating a new SQLite3 instance from the
     * filename given to the constructor initially
     */
    protected function openDatabase($databaseFileName = NULL) {
        $this->database = new SQLite3($databaseFileName);
        assert($this->database);
    }

    //==========================================================================
    // Private methods
    //==========================================================================

    /**
     * This method returns information about the given table name
     */
    private function columnsInformationWithTableName($sTableName) {
        // Setting the query
        $sQueryColumns = "PRAGMA table_info(':name')";
        $sQueryColumns = str_replace(':name', $sTableName, $sQueryColumns);

        // Preparing the query
        $oResult = $this->database->query($sQueryColumns);

        // Fetching result and preparing formatting of the result to a 
        // convenient usable format.
        $aResult = array();
        while ($aRow = $oResult->fetchArray(SQLITE3_ASSOC)) {
            $aResult[] = $aRow;
        }

        return $aResult;
    }

    /**
     * This method returns information about the given table name
     */
    private function tablesInformation() {
        // Launch the query to find information about tables
        // of the database
        $sQueryTables = "SELECT * FROM sqlite_master WHERE type='table'";
        $uResult = $this->database->query($sQueryTables);

        // Fetching result and preparing formatting of the result to a 
        // convenient usable format.
        $aResult = array();
        while ($aRow = $uResult->fetchArray(SQLITE3_ASSOC)) {
            $aResult[] = $aRow;
        }

        return $aResult;
    }

    private function schemaInformation() {
        $aSchema = array();
        $aTables = $this->tablesInformation();
        foreach ($aTables as $aTableInformation) {
            if (!isset($aTableInformation['name'])) {
                throw new Exception();
            }

            $sTableName = $aTableInformation['name'];
            $aColumns = $this->columnsInformationWithTableName($sTableName);
            $aSchema[$sTableName] = $aColumns;

            unset($sTableName);
        }
        unset($aTables);
        return $aSchema;
    }

    private function dataInformation($sTableName) {

        $sQueryData = "SELECT * FROM `$sTableName`";
        $uResult = $this->database->query($sQueryData);

        // Fetching result and preparing formatting of the result to a 
        // convenient usable format.
        $aResult = array();
        while ($aRow = $uResult->fetchArray(SQLITE3_ASSOC)) {
            $aResult[] = $aRow;
        }

        return $aResult;
    }

    //==========================================================================
    // Public methods
    //==========================================================================

    /**
     * Main method that will export the SQLite Database to a JSON stirng format.
     */
    public function sql_select($table) {
        $aResult = array();
        $aResult = $this->dataInformation($table);

        return json_encode($aResult);
    }
}

?>