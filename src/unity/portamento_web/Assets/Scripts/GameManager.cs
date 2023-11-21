using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.Threading;
using System.Text;

public class GameManager : MonoBehaviour
{
    // PERCORSO DELL'ESEGUIBILE DI PYTHON, DA OTTENERE DURANTE L'INSTALLAZIONE MAGARI
    private string anaconda_activate_path = @"C:\Users\nicol\anaconda3\Scripts\activate";
    private string anaconda_env = "portamento";

    public string user = "nic";

    private Settings settings = new Settings();
    private static string PATHS_FILE_NAME = @"\last_path.csv";
    private static string PATH_CLUSTERS_INTERFACE_SCRIPT = @"\ide\PORTAMENTO\PORTAMENTO\clusters_interface.py";

    public GameObject cluster_prefab;

    // UI LINKS
    public GameObject cluster_menu;
    private GameObject cluster_shown;
    public int cluster_menu_page;
    public GameObject display_menu;
    public GameObject map_menu;
    public GameObject map;
    private GameObject song_menu;

    private string current_path = System.IO.Directory.GetCurrentDirectory();
    public string root_path;
    public int n_clusters;

    private Dictionary<string, string> paths = new Dictionary<string, string>();
    public Dictionary<string, string> axis = new Dictionary<string, string>();
    public Dictionary<string, float> starting_centroid = new Dictionary<string, float>();

    private void Awake()
    {
        UnityEngine.Debug.Log("Current path: " + current_path);
        if (Application.isEditor) { 
            root_path = current_path.Remove(current_path.Length - 27);  // 27 PERCHE' QUESTO E' IL NUMERO DI CARATTERI DA CANCELLARE PER OTTENERE IL base_path A PARTIRE DAL PATH DEL PROGETTO
        } else { // SE STIAMO USANDO LA BUILD
            root_path = current_path.Remove(current_path.Length - 5);  // 5 SUPPONENDO CHE LA BUILD STIA NELLA CARTELLA /Play DI PORTAMENTO
        }
        string last_path_file = string.Concat(root_path, PATHS_FILE_NAME);

        paths = strings_csv_to_dict(last_path_file)[0];
        // OTTENGO LE INFORMAZIONI DI IMPOSTAZIONE
        settings.get_settings(paths["settings"]);   // Ottengo le settings

        cluster_menu.GetComponent<Canvas>().enabled = false;
        song_menu = cluster_menu.transform.GetChild(0).gameObject;
    }

    // Start is called before the first frame update
    void Start()
    {
        List<Dictionary<string, float>> centroids;
        List<Dictionary<string, float>> track_data;
        List<Dictionary<string, float>> track_radars;
        List<Dictionary<string, string>> meta_data;
        List<Dictionary<string, string>> meta_radars;
        List<Dictionary<string, string>> axis_packs;
        string clusters_path;

        clusters_path = paths["track_clust"];

        // ********************* DA QUI ESTRAPOLO LE INFORMAZIONI NEI .CSV
        axis_packs = strings_csv_to_dict(paths["axis_table"]);
        axis = select_axis(axis_packs, settings.axis);
        display_menu.GetComponent<DisplayMenu>().set_axis_labels(axis["axis1"], axis["axis2"], axis["axis3"]);

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
            cluster.GetComponent<Cluster>().set_id(i.ToString());
            cluster.GetComponent<Cluster>().set_is_leaf(is_leaf_bool);
            cluster.GetComponent<Cluster>().set_centroid(centroids[i]);
            cluster.GetComponent<Cluster>().set_cluster_data(track_data, meta_data);
            cluster.GetComponent<Cluster>().set_axis(axis["axis1"], axis["axis2"], axis["axis3"]);
            map.GetComponent<MapController>().append_cluster(cluster);
        }

        track_radars = floats_csv_to_dict(clusters_path + @"\radar_track.csv");
        meta_radars = strings_csv_to_dict(clusters_path + @"\radar_meta.csv");

        starting_centroid = centroids[(int)track_radars[0]["label"]];
        map.GetComponent<MapController>().set_radars(track_radars, meta_radars);
        
        // DO I PARAMETRI DELLE CANZONI ALLA MAPPA
        int j = 0;
        foreach(string key in centroids[0].Keys)
        {
            map.GetComponent<MapController>().append_axis(key);

            if (key == axis["axis1"])   // COME PREDEFINITO VOGLIAMO I PRIMI DUE ASSI DELLO SPAZIO
                map.GetComponent<MapController>().set_x(j);
            if (key == axis["axis2"])
                map.GetComponent<MapController>().set_y(j);

            j++;
        }

        map.GetComponent<MapController>().createMap();
        map.GetComponent<MapController>().launch_button_from_index((int)track_radars[0]["label"]);
        map_menu.GetComponent<Canvas>().enabled = false;
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void view_map()
    {
        map_menu.GetComponent<Canvas>().enabled = true;
        display_menu.SetActive(false);
    }

    public void close_map()
    {
        map_menu.GetComponent<Canvas>().enabled = false;
        display_menu.SetActive(true);
    }

    public string start_songMenu(GameObject cluster)
    {
        cluster_menu_page = 0;
        cluster_shown = cluster;
        List<Dictionary<string, string>> cluster_meta = cluster.GetComponent<Cluster>().meta;
        List<Dictionary<string, float>> cluster_track = cluster.GetComponent<Cluster>().track;
        Dictionary<string, float> centroid = cluster.GetComponent<Cluster>().centroid;
        string clusterID = cluster.GetComponent<Cluster>().get_id();
        bool is_leaf = cluster.GetComponent<Cluster>().is_leaf;
        cluster_menu.GetComponent<Canvas>().enabled = true;
        display_menu.SetActive(false);
        song_menu.GetComponent<SongMenu>().CreateMenu(is_leaf, clusterID, cluster_meta, cluster_track, centroid);
        return clusterID;
    }

    public void changepage_songMenu(int page)
    {
        cluster_menu_page = page;
        GameObject cluster = cluster_shown;
        List<Dictionary<string, string>> cluster_meta = cluster.GetComponent<Cluster>().meta;
        List<Dictionary<string, float>> cluster_track = cluster.GetComponent<Cluster>().track;
        Dictionary<string, float> centroid = cluster.GetComponent<Cluster>().centroid;
        string clusterID = cluster.GetComponent<Cluster>().get_id();
        bool is_leaf = cluster.GetComponent<Cluster>().is_leaf;
        cluster_menu.GetComponent<Canvas>().enabled = true;
        display_menu.SetActive(false);
        song_menu.GetComponent<SongMenu>().CreateMenu(is_leaf, clusterID, cluster_meta, cluster_track, centroid, page);
    }

    public void stop_songMenu()
    {
        cluster_menu.GetComponent<Canvas>().enabled = false;
        display_menu.SetActive(true);
        song_menu.GetComponent<SongMenu>().CancelMenu();
    }

    private List<Dictionary<string, string>> strings_csv_to_dict(string path_csv)
    {
        List<Dictionary<string, string>> dict = new List<Dictionary<string, string>>();
        string temp_key = "error";
        string temp_value = "error";

        // LETTURA E FORMATTAZIONE DEL FILE
        string file_data = System.IO.File.ReadAllText(path_csv);    // Leggo l'intero file
        file_data = file_data.Replace("\r", string.Empty);  // tolgo i caratteri \r di fine riga perchè in windows il fine riga è indicato con \r\n e non solo \n
        file_data = file_data.Replace("\"", string.Empty);  // compaiono anche di questi caratteri \" per qualche motivo
        file_data = file_data.Replace(", ", "<COMMA> ");  // per evitare che virgole di punteggiatura si confondano con le , che separano i campi. Dopo le risostituisco.

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

                temp_value = temp_value.Replace("<COMMA> ", ", ");
                
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
        string process_path = @"CMD.exe";
        string script_path = string.Concat(root_path, PATH_CLUSTERS_INTERFACE_SCRIPT);
        string script_arguments = string.Concat(current_cluster_id, " ", user);
        string process_arguments = string.Concat(@"/C ", anaconda_activate_path, " ", anaconda_env, " && ", "python ", script_path, " ", script_arguments);
        // '/C' è molto importante qui: senza di quello non funziona e deve precedere i comandi da dare al prompt

        var psi = new ProcessStartInfo();
        psi.FileName = process_path;
        psi.Arguments = process_arguments;

        // Process config
        psi.UseShellExecute = false;
        psi.CreateNoWindow = true;
        psi.RedirectStandardOutput = true;
        psi.RedirectStandardError = true;

        // Execute process and get output
        var results = "nothing";
        var errors = "nothing";

        UnityEngine.Debug.Log("Process: " + process_arguments);

        using (var process = Process.Start(psi))
        {
            process.WaitForExit();
            results = process.StandardOutput.ReadToEnd();
            errors = process.StandardError.ReadToEnd();
        }

        StringBuilder buffy = new StringBuilder();
        buffy.Append(results);
        buffy.Append("\n\n");
        buffy.Append(errors);

        UnityEngine.Debug.Log("Script: " + buffy.ToString());
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