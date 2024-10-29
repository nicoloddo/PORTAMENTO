using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.Text;
using UnityEngine.Networking;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using System.Linq;

public class GameManager : MonoBehaviour
{
    public GameObject cluster_prefab;

    /* UI References */

    // Environment axis and starting centroid
    public Dictionary<string, string> axis;
    public Dictionary<string, float> firstCentroid = new Dictionary<string, float>();

    // Clusters
    public GameObject cluster_menu;
    private GameObject cluster_shown;
    public int cluster_menu_page;
    public GameObject display_menu;

    // Map
    public GameObject map_menu;
    public GameObject map;

    // Song Menu
    private GameObject song_menu;

    /* API FETCHING */
    private string apiBaseUrl;
    private string apiKey;
    private string modelId = "9a5a63d8-6113-461c-9bb0-e0ba363a8b21-1730202855"; // Default model ID
    private const int MAX_RETRIES = 3;
    public bool fetched_node_data = false;

    private void Awake()
    {
        /* Set default settings */
        
        // Set default axis
        axis = new Dictionary<string, string>();
        axis["x"] = "valence";
        axis["y"] = "energy";
        axis["z"] = "danceability";

        // Initialize song menu
        song_menu = cluster_menu.transform.GetChild(0).gameObject;
    }

    // Initialization
    async void Start()
    {
        load_secrets();
        if (string.IsNullOrEmpty(apiKey) || string.IsNullOrEmpty(apiBaseUrl))
        {
            UnityEngine.Debug.LogError("Failed to load API credentials from secrets.txt");
            return;
        }

        // Fetch initial cluster data
        string current_node_id = PlayerPrefs.GetString("current_node_id", "0");
        JObject nodeData = await fetch_node_data(current_node_id);
        if (nodeData == null)
        {
            UnityEngine.Debug.LogError("Failed to fetch cluster data");
            return;
        }
        fetched_node_data = true;

        // Set up display menu axis labels (using fixed axes)
        display_menu.GetComponent<DisplayMenu>().set_axis_labels(axis["x"], axis["y"], axis["z"]);

        // Process cluster data
        JArray children = (JArray)nodeData["children"];

        // Initialize radar data, the most popular song in each cluster will be added to this
        List<Dictionary<string, float>> radar_track = new List<Dictionary<string, float>>();
        List<Dictionary<string, string>> radar_meta = new List<Dictionary<string, string>>();

        // Process and Instantiate the clusters
        int cluster_index = 0;
        foreach (JObject child in children)
        {
            // Create centroid dictionary from child data
            Dictionary<string, float> centroid = child["centroid"].ToObject<Dictionary<string, float>>();

            // Retrieve the data for this cluster
            List<Dictionary<string, float>> track = child["track"].ToObject<List<Dictionary<string, float>>>();
            List<Dictionary<string, string>> meta = child["meta"].ToObject<List<Dictionary<string, string>>>();

            // Verify track and meta lists have matching lengths
            if (track.Count != meta.Count)
            {
                UnityEngine.Debug.LogError($"Track and meta data length mismatch for cluster {cluster_index}. Track: {track.Count}, Meta: {meta.Count}");
                return;
            }

            // Get the most popular song in this child cluster to build the radar data
            string most_popular_id = child["most_popular_id"].ToString();
            int popular_index = meta.FindIndex(m => m["id"] == most_popular_id);

            Dictionary<string, float> most_popular_track = track[popular_index];
            Dictionary<string, string> most_popular_meta = meta[popular_index];

            // Add the most popular song in the cluster to the radar data
            most_popular_track["label"] = cluster_index;
            radar_track.Add(most_popular_track);
            radar_meta.Add(most_popular_meta);

            // Instantiate cluster and populate with data
            GameObject cluster = Instantiate(cluster_prefab);
            cluster.GetComponent<Cluster>().set_id(cluster_index.ToString());
            cluster.GetComponent<Cluster>().set_is_leaf((bool)child["is_leaf"]);
            cluster.GetComponent<Cluster>().set_centroid(centroid);
            cluster.GetComponent<Cluster>().set_axis(axis["x"], axis["y"], axis["z"]);
            cluster.GetComponent<Cluster>().set_cluster_data(track, meta);
            map.GetComponent<MapController>().append_cluster(cluster);

            cluster_index++;
        }
        
        // Configure map with song parameters
        firstCentroid = ((JObject)children[0]["centroid"]).ToObject<Dictionary<string, float>>();
        int j = 0;
        foreach (string key in firstCentroid.Keys)
        {
            map.GetComponent<MapController>().append_axis(key);

            if (key == axis["x"])   // Default to first two axes of the space
                map.GetComponent<MapController>().set_x(j);
            if (key == axis["y"])
                map.GetComponent<MapController>().set_y(j);

            j++;
        }

        // Set the radars
        map.GetComponent<MapController>().set_radars(radar_track, radar_meta);
        map.GetComponent<MapController>().createMap();
        map.GetComponent<MapController>().select_cluster_from_index((int)radar_track[0]["label"]);
        map_menu.GetComponent<Canvas>().enabled = false;
    }

    // Update is called once per frame
    void Update()
    {

    }

    private async Task<JObject> fetch_node_data(string nodeId, int retryCount = 0)
    {
        if (retryCount >= MAX_RETRIES)
        {
            UnityEngine.Debug.LogError("Max retries reached when fetching node data");
            return null;
        }

        using (UnityWebRequest request = UnityWebRequest.Get($"{apiBaseUrl}/nav"))
        {
            // Set headers
            request.SetRequestHeader("x-api-key", apiKey);
            request.SetRequestHeader("Content-Type", "application/json");
            request.SetRequestHeader("model-id", modelId);
            request.SetRequestHeader("node-id", nodeId);

            var operation = request.SendWebRequest();
            while (!operation.isDone)
                await Task.Yield();

            if (request.result != UnityWebRequest.Result.Success)
            {
                UnityEngine.Debug.LogWarning($"Request failed (attempt {retryCount + 1}): {request.error}");
                // Retry with exponential backoff
                await Task.Delay((retryCount + 1) * 1000);
                return await fetch_node_data(nodeId, retryCount + 1);
            }

            string jsonResponse = request.downloadHandler.text;
            return JObject.Parse(jsonResponse);
        }
    }

    private void load_secrets()
    {
        string[] lines = System.IO.File.ReadAllLines(Application.dataPath + "/secrets.txt");
        foreach (string line in lines)
        {
            string[] parts = line.Split('=');
            if (parts.Length == 2)
            {
                if (parts[0] == "API_KEY")
                    apiKey = parts[1].Trim();
                else if (parts[0] == "API_BASE_URL")
                    apiBaseUrl = parts[1].Trim();
            }
        }
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

    private Dictionary<string, string> select_axis(List<Dictionary<string, string>> dicts, string id)
    {
        foreach (Dictionary<string, string> dict in dicts)
        {
            if (dict["id"] == id)
                return dict;
        }
        throw new System.Exception("No dictionary found with the specified id.");
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
