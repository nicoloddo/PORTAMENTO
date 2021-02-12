using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public string user = "nic";

    private Settings settings = new Settings();
    private static string PATHS_FILE_NAME = @"\last_path.csv";
    private static string PATH_CLUSTERS_INTERFACE_SCRIPT = @"\ide\PORTAMENTO\PORTAMENTO\clusters_interface.py";

    public GameObject cluster_prefab;

    private string current_path = System.IO.Directory.GetCurrentDirectory();
    public string root_path;
    public int n_clusters;

    Dictionary<string, string> paths = new Dictionary<string, string>();

    private void Awake()
    {
        root_path = current_path.Remove(current_path.Length - 27);  // 27 PERCHE' QUESTO E' IL NUMERO DI CARATTERI DA CANCELLARE PER OTTENERE IL base_path
        string last_path_file = string.Concat(root_path, PATHS_FILE_NAME);

        paths = strings_csv_to_dict(last_path_file)[0];
        // OTTENGO LE INFORMAZIONI DI IMPOSTAZIONE
        settings.get_settings(paths["settings"]);   // Ottengo le settings
    }

    // Start is called before the first frame update
    void Start()
    {
        List<Dictionary<string, float>> centroids;
        List<Dictionary<string, float>> track_data;
        List<Dictionary<string, string>> meta_data;
        List<Dictionary<string, string>> axis_packs;
        Dictionary<string, string> axis;
        string clusters_path;

        clusters_path = paths["track_clust"];

        // ********************* DA QUI ESTRAPOLO LE INFORMAZIONI NEI .CSV
        axis_packs = strings_csv_to_dict(paths["axis_table"]);
        axis = select_axis(axis_packs, settings.axis);

        // OTTENGO I CENTROIDI
        centroids = floats_csv_to_dict(clusters_path + @"\centroids.csv");

        n_clusters = centroids.Count;

        for(int i = 0; i < n_clusters; i++)
        {
            // OTTENGO LE INFORMAZIONI TRACK E META DAI CSV
            track_data = floats_csv_to_dict(clusters_path + @"\track" + i.ToString() + @".csv");
            meta_data = strings_csv_to_dict(clusters_path + @"\meta" + i.ToString() + @".csv");

            // CONVERTO L'INFORMAZIONE IS_LEAF
            // L'INFORMAZIONE IS_LEAF E' MOLTO IMPORTANTE PERCHE' SE UN CLUSTER E' FOGLIA, NON BISOGNA RIAVVIARE clusters_interface.py
            // BISOGNA INFATTI NELLA PROSSIMA SCENA MOSTRARE TUTTE LE CANZONI APPARTENENTI AL CLUSTER E NON ALTRI CLUSTER.
            float is_leaf = centroids[i]["is_leaf"];
            bool is_leaf_bool = false;
            centroids[i].Remove("is_leaf");
            switch(is_leaf)
            {
                case 0:
                    is_leaf_bool = false;
                    break;
                case 1:
                    is_leaf_bool = true;
                    break;
                default:
                    throw new System.Exception("Il valore di is_leaf non era nè 1 nè 0.");
                    // break;
            }


            // ISTANZIO IL CLUSTER E INSERISCO LE INFORMAZIONI
            GameObject cluster = Instantiate(cluster_prefab);
            cluster.GetComponent<Cluster>().set_is_leaf(is_leaf_bool);
            cluster.GetComponent<Cluster>().set_centroid(centroids[i]);
            cluster.GetComponent<Cluster>().set_cluster_data(track_data, meta_data);
            cluster.GetComponent<Cluster>().set_axis(axis["axis1"], axis["axis2"], axis["axis3"]);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private List<Dictionary<string, string>> strings_csv_to_dict(string path_csv)
    {
        List<Dictionary<string, string>> dict = new List<Dictionary<string, string>>();
        string temp_key = "error";
        string temp_value = "error";

        // LETTURA E FORMATTAZIONE DEL FILE
        string file_data = System.IO.File.ReadAllText(path_csv);    // Leggo l'intero file
        file_data = file_data.Replace("\r", string.Empty);  // tolgo i caratteri \r di fine riga perchè in windows il fine riga è indicato con \r\n e non solo \n

        string[] splitted = file_data.Split('\n');  // Ora il fine riga è indicato solo con \n, posso separare secondo quel carattere
        System.Array.Resize(ref splitted, splitted.Length - 1); // tolgo l'ultimo elemento che è una stringa vuota
        string[] keys = splitted[0].Split(','); // Ogni campo è separato da una virgola. La prima riga del csv indica il nome delle colonne, ossia le keys
        
        // INSERIMENTO NELLA LISTA DI DIZIONARI
        for (int i = 0; i < splitted.Length - 1; i++)   // Lenght-1 perchè nell'iterazione abbiamo i+1
        {
            Dictionary<string, string> dict_row = new Dictionary<string, string>(); // dizionario temporaneo per ogni elemento della lista di dizionari
            for (int j = 0; j < keys.Length; j++)
            {
                temp_key = keys[j];
                temp_value = splitted[i + 1].Split(',')[j]; // i+1 perchè la prima riga è occupata dai nomi delle keys
                
                dict_row.Add(temp_key, temp_value);
            }
            
            dict.Add(dict_row); 
        }

        return dict;
    }

    private List<Dictionary<string, float>> floats_csv_to_dict(string path_csv)
    {
        List<Dictionary<string, float>> dicts = new List<Dictionary<string, float>>();
        string temp_key = "error";
        string temp_string = "error";
        float temp_value = -1;

        // LETTURA E FORMATTAZIONE DEL FILE
        string file_data = System.IO.File.ReadAllText(path_csv);    // Leggo l'intero file
        file_data = file_data.Replace("\r", string.Empty);  // tolgo i caratteri \r di fine riga perchè in windows il fine riga è indicato con \r\n e non solo \n

        string[] splitted = file_data.Split('\n');  // Ora il fine riga è indicato solo con \n, posso separare secondo quel carattere
        System.Array.Resize(ref splitted, splitted.Length - 1); // tolgo l'ultimo elemento che è una stringa vuota
        string[] keys = splitted[0].Split(','); // Ogni campo è separato da una virgola. La prima riga del csv indica il nome delle colonne, ossia le keys

        // INSERIMENTO NELLA LISTA DI DIZIONARI
        for (int i = 0; i < splitted.Length - 1; i++)   // Lenght-1 perchè nell'iterazione abbiamo i+1
        {
            Dictionary<string, float> dict_row = new Dictionary<string, float>(); // dizionario temporaneo per ogni elemento della lista di dizionari
            for (int j = 0; j < keys.Length; j++)
            {
                temp_key = keys[j];
                temp_string = splitted[i + 1].Split(',')[j]; // i+1 perchè la prima riga è occupata dai nomi delle keys
                // Converto la stringa in un float
                temp_value = float.Parse(temp_string, System.Globalization.CultureInfo.InvariantCulture.NumberFormat);

                dict_row.Add(temp_key, temp_value);
            }

            dicts.Add(dict_row);
        }

        return dicts;
    }

    private Dictionary<string, string> select_axis(List<Dictionary<string, string>> dicts, string id)
    {
        foreach (Dictionary<string, string> dict in dicts)
        {
            if (dict["id"] == id)
                return dict;
        }
        throw new System.Exception("Nessun dict ha questo id.");
    }

    public void runClustersInterface(string current_cluster_id)
    {
        string process_path = string.Concat(root_path, PATH_CLUSTERS_INTERFACE_SCRIPT);
        string process_arguments = string.Concat(current_cluster_id, " ", user);
        System.Diagnostics.Process process = new System.Diagnostics.Process();

        process.StartInfo.FileName = process_path;
        process.StartInfo.Arguments = process_arguments;

        //use to create no window when running cmd script
        process.StartInfo.UseShellExecute = true;
        process.StartInfo.CreateNoWindow = true;
        process.StartInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;

        process.Start();

        //if you want program to halt until script is finished
        process.WaitForExit();
    }
}

[System.Serializable]
public class Settings
{
    public string axis;
    public string dataset;
    public string weights;

    public void get_settings(string path)
    {
        string json = System.IO.File.ReadAllText(path);    // Leggo l'intero file
        JsonUtility.FromJsonOverwrite(json, this);
    }
}