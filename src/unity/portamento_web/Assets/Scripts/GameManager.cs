using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.Threading;
using System.Text;

public class GameManager : MonoBehaviour
{
    // Path to Python executable, to be configured during installation
    private string anaconda_activate_path = @"C:\Users\nicol\anaconda3\Scripts\activate";
    private string anaconda_env = "portamento";

    public string user = "nic";

    private Settings settings = new Settings();
    private static string PATHS_FILE_NAME = @"\last_path.csv";
    private static string PATH_CLUSTERS_INTERFACE_SCRIPT = @"\ide\PORTAMENTO\PORTAMENTO\clusters_interface.py";

    public GameObject cluster_prefab;

    // UI References
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
            root_path = current_path.Remove(current_path.Length - 27);  // Remove 27 characters to obtain the base_path from the project path
        } else { // When using the build
            root_path = current_path.Remove(current_path.Length - 5);  // Assuming the build is in the /Play folder of PORTAMENTO
        }
        string last_path_file = string.Concat(root_path, PATHS_FILE_NAME);

        paths = strings_csv_to_dict(last_path_file)[0];
        // Retrieve setting information
        settings.get_settings(paths["settings"]);   // Obtain the settings

        cluster_menu.GetComponent<Canvas>().enabled = false;
        song_menu = cluster_menu.transform.GetChild(0).gameObject;
    }

    // Initialization
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

        // Extract information from CSV files
        axis_packs = strings_csv_to_dict(paths["axis_table"]);
        axis = select_axis(axis_packs, settings.axis);
        display_menu.GetComponent<DisplayMenu>().set_axis_labels(axis["axis1"], axis["axis2"], axis["axis3"]);

        // Retrieve centroids
        centroids = floats_csv_to_dict(clusters_path + @"\centroids.csv");

        n_clusters = centroids.Count;

        for(int i = 0; i < n_clusters; i++)
        {
            // Retrieve track and meta information from CSV
            track_data = floats_csv_to_dict(clusters_path + @"\track" + i.ToString() + @".csv");
            meta_data = strings_csv_to_dict(clusters_path + @"\meta" + i.ToString() + @".csv");

            // Process is_leaf information
            // This is crucial as it determines whether to restart clusters_interface.py
            // For leaf clusters, we display all songs in the cluster rather than sub-clusters
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
                    throw new System.Exception("Invalid value for is_leaf: expected 0 or 1.");
            }


            // Instantiate cluster and populate with data
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
        
        // Configure map with song parameters
        int j = 0;
        foreach(string key in centroids[0].Keys)
        {
            map.GetComponent<MapController>().append_axis(key);

            if (key == axis["axis1"])   // Default to first two axes of the space
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

        // Read and process the file
        string file_data = System.IO.File.ReadAllText(path_csv);    // Read the entire file
        file_data = file_data.Replace("\r", string.Empty);  // Remove \r characters from line endings (Windows uses \r\n)
        file_data = file_data.Replace("\"", string.Empty);  // Remove extraneous quotation marks
        file_data = file_data.Replace(", ", "<COMMA> ");  // Temporarily replace commas in data to avoid confusion with field separators

        string[] splitted = file_data.Split('\n');  // Split by newline character
        System.Array.Resize(ref splitted, splitted.Length - 1); // Remove the last empty element
        string[] keys = splitted[0].Split(','); // First row contains column names (keys)
        
        // Populate the list of dictionaries
        for (int i = 0; i < splitted.Length - 1; i++)   // Length-1 because we use i+1 in the loop
        {
            Dictionary<string, string> dict_row = new Dictionary<string, string>(); // Temporary dictionary for each row
            for (int j = 0; j < keys.Length; j++)
            {
                temp_key = keys[j];
                temp_value = splitted[i + 1].Split(',')[j]; // i+1 to skip the header row

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

        // Read and process the file
        string file_data = System.IO.File.ReadAllText(path_csv);    // Read the entire file
        file_data = file_data.Replace("\r", string.Empty);  // Remove \r characters from line endings (Windows uses \r\n)

        string[] splitted = file_data.Split('\n');  // Split by newline character
        System.Array.Resize(ref splitted, splitted.Length - 1); // Remove the last empty element
        string[] keys = splitted[0].Split(','); // First row contains column names (keys)

        // Populate the list of dictionaries
        for (int i = 0; i < splitted.Length - 1; i++)   // Length-1 because we use i+1 in the loop
        {
            Dictionary<string, float> dict_row = new Dictionary<string, float>(); // Temporary dictionary for each row
            for (int j = 0; j < keys.Length; j++)
            {
                temp_key = keys[j];
                temp_string = splitted[i + 1].Split(',')[j]; // i+1 to skip the header row
                // Convert the string to a float
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
        throw new System.Exception("No dictionary found with the specified id.");
    }

    public void runClustersInterface(string current_cluster_id)
    {
        string process_path = @"CMD.exe";
        string script_path = string.Concat(root_path, PATH_CLUSTERS_INTERFACE_SCRIPT);
        string script_arguments = string.Concat(current_cluster_id, " ", user);
        string process_arguments = string.Concat(@"/C ", anaconda_activate_path, " ", anaconda_env, " && ", "python ", script_path, " ", script_arguments);
        // '/C' is crucial here: it must precede the commands for the prompt to execute them

        var psi = new ProcessStartInfo();
        psi.FileName = process_path;
        psi.Arguments = process_arguments;

        // Process configuration
        psi.UseShellExecute = false;
        psi.CreateNoWindow = true;
        psi.RedirectStandardOutput = true;
        psi.RedirectStandardError = true;

        // Execute process and capture output
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

        UnityEngine.Debug.Log("Script output: " + buffy.ToString());
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
        string json = System.IO.File.ReadAllText(path);    // Read the entire file
        JsonUtility.FromJsonOverwrite(json, this);
    }
}