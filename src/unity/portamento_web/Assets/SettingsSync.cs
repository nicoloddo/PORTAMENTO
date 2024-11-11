using UnityEngine;
using UnityEngine.UI;
using System.Linq;

public class SettingsSync : MonoBehaviour
{
    [SerializeField] private string playerPrefKey;  // Key to identify which PlayerPref to sync
    [SerializeField] private int[] triggerValues;
    private int lastValue;  // Cache the last known value

    void Start()
    {
        // Initialize with current PlayerPref value
        lastValue = PlayerPrefs.GetInt(playerPrefKey, 0);
        UpdateComponent(lastValue);
    }

    void Update()
    {
        // Check if PlayerPref value has changed
        int currentValue = PlayerPrefs.GetInt(playerPrefKey, 0);
        if (currentValue != lastValue)
        {
            lastValue = currentValue;
            UpdateComponent(currentValue);
        }
    }

    private void UpdateComponent(int value)
    {
        if (playerPrefKey == "spotifyInstalled")
        {
            if (triggerValues.Contains(value))
            {
                GetComponentInChildren<Image>().color = new Color(1, 1, 1, 1);
            }
            else
            {
                GetComponentInChildren<Image>().color = new Color(0, 140f/255f, 1, 1);
            }
        }
    }
}
