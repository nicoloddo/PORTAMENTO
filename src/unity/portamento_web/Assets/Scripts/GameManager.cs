using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.Text;
using UnityEngine.Networking;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using System.Linq;
using BackendSettingsSpace;
using System;

public class GameManager : MonoBehaviour
{
    public bool DebuggingMode = false;
    public GameObject ClusterPrefab;

    /* UI References */
    // Environment axis and starting centroid
    public Dictionary<string, string> Axis;
    public Dictionary<string, float> FirstCentroid = new Dictionary<string, float>();

    // Clusters Controller
    public GameObject ClusterMenu;
    private GameObject _clusterShown;
    public int ClusterMenuPage;
    public GameObject DisplayMenu;

    // Other UI
    public StatusController StatusLabel;
    public GameObject MapMenu;
    public GameObject Map;
    public GameObject SettingsMenu;
    public GameObject ClusterSongsMenu;

    /* API FETCHING */
    private string _apiBaseUrl;
    private string _apiKey;
    private string _modelId; // Put the default model ID in the secrets.txt file
    private const int MAX_RETRIES = 3;
    private const int TOTAL_RADAR_SLOTS = 12;
    public bool FetchedNodeData = false;
    public bool FinishedLoading = false;

    private void Awake()
    {
        /* Set default settings */
        
        // Set default axis
        Axis = new Dictionary<string, string>();
        Axis["x"] = "valence";
        Axis["y"] = "energy";
        Axis["z"] = "danceability";

        // Initialize UI
        Cursor.visible = true;
        Cursor.lockState = CursorLockMode.None;
        SettingsMenu.GetComponent<MenuHider>().SetActive(false);
        ClusterMenu.GetComponent<MenuHider>().SetActive(false);
        MapMenu.GetComponent<MenuHider>().SetActive(false);
        DisplayMenu.GetComponent<MenuHider>().SetActive(false);
    }

    async void Start()
    {
        StatusLabel.manualMode = true;
        if (!DebuggingMode)
        {
            LoadBackendSettings();
            if (string.IsNullOrEmpty(_apiKey) || string.IsNullOrEmpty(_apiBaseUrl))
            {
                StatusLabel.SetStatus("Failed to load API credentials. You can contact me at https://github.com/nicoloddo");
                UnityEngine.Debug.LogError("Failed to load API credentials from secrets.txt");
                return;
            }

            // Fetch initial cluster data
            string currentNodeId = PlayerPrefs.GetString("current_node_id", "0");
            JObject nodeData = await FetchNodeData(currentNodeId);
            if (nodeData == null)
            {
                StatusLabel.SetStatus("Failed to fetch cluster data. You can contact me at https://github.com/nicoloddo");
                UnityEngine.Debug.LogError("Failed to fetch cluster data.");
                return;
            }
            FetchedNodeData = true;
            UnityEngine.Debug.Log("Fetched node data.");
            StatusLabel.SetStatus("");
            StatusLabel.manualMode = false;

            // Set up display menu axis labels (using fixed axes)
            DisplayMenu.GetComponent<DisplayMenu>().SetAxisLabels(Axis["x"], Axis["y"], Axis["z"]);

            // Process cluster data
            JArray children = (JArray)nodeData["children"];

            // Initialize radar data, the most popular song in each cluster will be added to this
            List<Dictionary<string, float>> radarTrack = new List<Dictionary<string, float>>();
            List<Dictionary<string, string>> radarMeta = new List<Dictionary<string, string>>();

            // Calculate songs per cluster if we have fewer than TOTAL_RADAR_SLOTS clusters
            int songsPerCluster = children.Count < TOTAL_RADAR_SLOTS 
                ? (int)Math.Ceiling((double)TOTAL_RADAR_SLOTS / children.Count)
                : 1;
                
            // Process and Instantiate the clusters
            int clusterIndex = 0;
            foreach (JObject child in children)
            {
                // Create centroid dictionary from child data
                Dictionary<string, float> centroid = child["centroid"].ToObject<Dictionary<string, float>>();

                // Retrieve the data for this cluster
                List<Dictionary<string, float>> track = child["track"].ToObject<List<Dictionary<string, float>>>();
                List<Dictionary<string, string>> meta = child["meta"].ToObject<List<Dictionary<string, string>>>();

                // Create a list of tuples to maintain the relationship while sorting
                var combined = track.Select((t, index) => new { Track = t, Meta = meta[index] })
                    .OrderByDescending(x => x.Track["distance"])
                    .ToList();

                // Split back into separate lists
                track = combined.Select(x => x.Track).ToList();
                meta = combined.Select(x => x.Meta).ToList();

                // Verify track and meta lists have matching lengths
                if (track.Count != meta.Count)
                {
                    UnityEngine.Debug.LogError($"Track and meta data length mismatch for cluster {clusterIndex}");
                    return;
                }

                // Get the most representative song in this child cluster to build the radar data
                string mostRepresentativeId = child["most_representative_id"].ToString();
                int representativeIndex = meta.FindIndex(m => m["id"] == mostRepresentativeId);

                Dictionary<string, float> mostRepresentativeTrack = track[representativeIndex];
                Dictionary<string, string> mostRepresentativeMeta = meta[representativeIndex];

                // Add up to songsPerCluster songs from this cluster to the radar data
                for (int i = 0; i < songsPerCluster && i < track.Count; i++)
                {
                    Dictionary<string, float> trackToAdd = i == 0 
                        ? mostRepresentativeTrack // First song is always the most representative
                        : track[i];
                    Dictionary<string, string> metaToAdd = i == 0
                        ? mostRepresentativeMeta
                        : meta[i];

                    trackToAdd["label"] = clusterIndex;
                    radarTrack.Add(trackToAdd);
                    radarMeta.Add(metaToAdd);

                    // Break if we've reached total radar slots
                    if (radarTrack.Count >= TOTAL_RADAR_SLOTS) break;
                }

                // Instantiate cluster and populate with data
                GameObject cluster = Instantiate(ClusterPrefab);
                cluster.GetComponent<Cluster>().SetId(clusterIndex.ToString());
                cluster.GetComponent<Cluster>().SetIsLeaf((bool)child["is_leaf"]);
                cluster.GetComponent<Cluster>().SetCentroid(centroid);
                cluster.GetComponent<Cluster>().SetAxis(Axis["x"], Axis["y"], Axis["z"]);
                cluster.GetComponent<Cluster>().SetClusterData(track, meta);
                Map.GetComponent<MapController>().AppendCluster(cluster);

                clusterIndex++;
            }
        
            // Configure map with song parameters
            FirstCentroid = ((JObject)children[0]["centroid"]).ToObject<Dictionary<string, float>>();
            int j = 0;
            foreach (string key in FirstCentroid.Keys)
            {
                Map.GetComponent<MapController>().AppendAxis(key);

                if (key == Axis["x"])   // Default to first two axes of the space
                    Map.GetComponent<MapController>().SetX(j);
                if (key == Axis["y"])
                    Map.GetComponent<MapController>().SetY(j);

                j++;
            }

            // Set the radars
            if (FetchedNodeData)
            {
                Map.GetComponent<MapController>().SetRadars(radarTrack, radarMeta);
                Map.GetComponent<MapController>().CreateMap();
                Map.GetComponent<MapController>().SelectClusterFromIndex((int)radarTrack[0]["label"]);
                MapMenu.GetComponent<MenuHider>().SetActive(false);
            }
        }

        // The clusters are fetched. Enable the relevant menus
        if (FetchedNodeData || DebuggingMode)
        {
            ClusterMenu.GetComponent<MenuHider>().SetActive(false);
            if (PlayerPrefs.HasKey("spotifyInstalled"))
            {
                SettingsMenu.GetComponent<MenuHider>().SetActive(true);
                MapMenu.GetComponent<MenuHider>().SetActive(false);
                DisplayMenu.GetComponent<MenuHider>().SetActive(true);
            }
            else
            {
                SettingsMenu.GetComponent<MenuHider>().SetActive(false);
                MapMenu.GetComponent<MenuHider>().SetActive(true);
                DisplayMenu.GetComponent<MenuHider>().SetActive(false);
            }
        }
        FinishedLoading = true;
    }

    private async Task<JObject> FetchNodeData(string nodeId, int retryCount = 0)
    {
        if (retryCount >= MAX_RETRIES)
        {
            StatusLabel.SetStatus("Max retries reached when fetching node data. You can contact me at https://github.com/nicoloddo");
            UnityEngine.Debug.LogError("Max retries reached when fetching node data");
            return null;
        }

        // First request to get the pre-signed URL
        using (UnityWebRequest request = UnityWebRequest.Get($"{_apiBaseUrl}/nav"))
        {
            request.SetRequestHeader("x-api-key", _apiKey);
            request.SetRequestHeader("Content-Type", "application/json");
            request.SetRequestHeader("model-id", _modelId);
            request.SetRequestHeader("node-id", nodeId);

            var operation = request.SendWebRequest();
            while (!operation.isDone)
                await Task.Yield();

            if (request.result != UnityWebRequest.Result.Success)
            {
                UnityEngine.Debug.LogWarning($"Request failed (attempt {retryCount + 1}): {request.error}");
                await Task.Delay((retryCount + 1) * 1000);
                return await FetchNodeData(nodeId, retryCount + 1);
            }

            // Parse the initial response to get the pre-signed URL
            string initialResponse = request.downloadHandler.text;
            JObject urlResponse = JObject.Parse(initialResponse);
            string presignedUrl = urlResponse["url"].ToString();
            
            // Second request to get the actual data using the pre-signed URL
            using (UnityWebRequest dataRequest = UnityWebRequest.Get(presignedUrl))
            {
                var dataOperation = dataRequest.SendWebRequest();
                while (!dataOperation.isDone)
                    await Task.Yield();

                if (dataRequest.result != UnityWebRequest.Result.Success)
                {
                    UnityEngine.Debug.LogWarning($"Data fetch failed (attempt {retryCount + 1}): {dataRequest.error}");
                    await Task.Delay((retryCount + 1) * 1000);
                    return await FetchNodeData(nodeId, retryCount + 1);
                }

                string jsonResponse = dataRequest.downloadHandler.text;
                return JObject.Parse(jsonResponse);
            }
        }
    }

    private void LoadBackendSettings()
    {
        _apiKey = BackendSettings.ApiKey;
        _apiBaseUrl = BackendSettings.ApiBaseUrl;
        _modelId = BackendSettings.ModelId;
    }

    public void ViewMap()
    {
        Cursor.visible = true;
        Cursor.lockState = CursorLockMode.None;
        MapMenu.GetComponent<MenuHider>().SetActive(true);
        DisplayMenu.GetComponent<MenuHider>().SetActive(false);
    }

    public void CloseMap()
    {
        Cursor.visible = false;
        Cursor.lockState = CursorLockMode.Locked;
        MapMenu.GetComponent<MenuHider>().SetActive(false);
        DisplayMenu.GetComponent<MenuHider>().SetActive(true);
    }

    public string StartSongMenu(GameObject cluster)
    {
        Cursor.visible = true;
        Cursor.lockState = CursorLockMode.None;
        ClusterMenuPage = 0;
        _clusterShown = cluster;
        List<Dictionary<string, string>> clusterMeta = cluster.GetComponent<Cluster>().Meta;
        List<Dictionary<string, float>> clusterTrack = cluster.GetComponent<Cluster>().Track;
        Dictionary<string, float> centroid = cluster.GetComponent<Cluster>().Centroid;
        string clusterId = cluster.GetComponent<Cluster>().GetId();
        bool isLeaf = cluster.GetComponent<Cluster>().IsLeaf;
        ClusterMenu.GetComponent<MenuHider>().SetActive(true);
        DisplayMenu.GetComponent<MenuHider>().SetActive(false);
        ClusterSongsMenu.GetComponent<SongMenu>().CreateMenu(isLeaf, clusterId, clusterMeta, clusterTrack, centroid);
        return clusterId;
    }

    public void ChangePageSongMenu(int page)
    {
        ClusterMenuPage = page;
        GameObject cluster = _clusterShown;
        List<Dictionary<string, string>> clusterMeta = cluster.GetComponent<Cluster>().Meta;
        List<Dictionary<string, float>> clusterTrack = cluster.GetComponent<Cluster>().Track;
        Dictionary<string, float> centroid = cluster.GetComponent<Cluster>().Centroid;
        string clusterId = cluster.GetComponent<Cluster>().GetId();
        bool isLeaf = cluster.GetComponent<Cluster>().IsLeaf;
        ClusterMenu.GetComponent<MenuHider>().SetActive(true);
        DisplayMenu.GetComponent<MenuHider>().SetActive(false);
        ClusterSongsMenu.GetComponent<SongMenu>().CreateMenu(isLeaf, clusterId, clusterMeta, clusterTrack, centroid, page);
    }

    public void StopSongMenu()
    {
        Cursor.visible = false;
        Cursor.lockState = CursorLockMode.Locked;
        ClusterMenu.GetComponent<MenuHider>().SetActive(false);
        DisplayMenu.GetComponent<MenuHider>().SetActive(true);
        ClusterSongsMenu.GetComponent<SongMenu>().CancelMenu();
    }

    private Dictionary<string, string> SelectAxis(List<Dictionary<string, string>> dicts, string id)
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
