using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerController : MonoBehaviour
{
    int axis_multiplier = 400; // Also present in SongMenu, DisplayMenu and Cluster classes: used to space out clusters

    // USEFUL ASSIGNMENTS
    private Animator animator;
    private CharacterController characterController;
    public Vector3 lookat_rotation;

    // INPUT DELAY
    float just_pressed = 0; // Used to wait before receiving a new input. Prevents immediate menu closure if pressed slightly too long
    float just_pressed_max = 0.1f;

    // REFERENCES
    public new GameObject camera;
    private GameManager gameManager;
    private GameObject nearCluster;

    // STATE FLAGS
    private bool first_run = true;
    public bool is_near = false;
    public bool can_move = true;
    private bool song_menu_opened = false;
    private bool map_opened = false;

    // INPUT VARIABLES
    private float inputUpward; // For upward movement
    private float inputVertical; // Keys for forward movement
    private float inputHorizontal; // Keys for rotation (in addition to mouse)
    public float totalXRot; // Total X rotation
    public float totalYRot; // Total Y rotation

    // MOVEMENT PARAMETERS
    private float rotateSpeedX = 4f; // X rotation speed
    private float rotateSpeedY = 3f; // Y rotation speed
    public float forwardSpeed = 0.8f; // Forward movement speed
    public float lateralSpeed = 0.5f; // Lateral movement speed
    public float upwardSpeed = 0.5f; // Upward movement speed

    // NAVIGATION
    public string current_cluster_id = "0";
    public Transform selected_clust_transform;

    private void Awake()
    {
        gameManager = FindObjectOfType<GameManager>();
        animator = GetComponent<Animator>();
        characterController = GetComponent<CharacterController>();
    }

    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        if (!gameManager.fetched_node_data)
            return;

        if(just_pressed < just_pressed_max + 5)
        just_pressed += Time.deltaTime;

        if (first_run)
        {
            // Disable and re-enable the character controller to allow teleportation
            gameObject.GetComponent<CharacterController>().enabled = false;
            transform.position = get_start();
            first_run = false;
            gameObject.GetComponent<CharacterController>().enabled = true;
        }

        if (Input.GetKey("f") && is_near && !map_opened && just_pressed > just_pressed_max)
        {
            if(!song_menu_opened)
            {
                song_menu_run();
                animator.SetFloat("fly", 0);    // Stop the player
                just_pressed = 0;   // Start the timer
            }
            else if(just_pressed > 1)
            {
                song_menu_esc();
                just_pressed = 0;   // Start the timer
            }  
        }

        if (Input.GetKey("m") && !song_menu_opened && just_pressed > just_pressed_max)
        {
            if (!map_opened)
            {
                map_show();
                animator.SetFloat("fly", 0);    // Stop the player
                just_pressed = 0;   // Start the timer
            }
            else if (just_pressed > 1)
            {
                map_esc();
                just_pressed = 0;   // Start the timer
            }
        }

        if (Input.GetKey("r") && !song_menu_opened && !map_opened)
        {
            transform.LookAt(selected_clust_transform);
            totalXRot = transform.rotation.eulerAngles.y;
            totalYRot = transform.rotation.eulerAngles.x;
        }

        if (Input.GetKey("z") && !song_menu_opened && !map_opened)
        {
            totalYRot = 0;
        }

        if (Input.GetKey("x") && !song_menu_opened && !map_opened)
        {
            if (!Input.GetKey(KeyCode.LeftControl))
            {
                totalXRot = 90;
                totalYRot = 0;
            }
            if (Input.GetKey(KeyCode.LeftControl))
            {
                totalXRot = -90;
                totalYRot = 0;
            }
        }

        if (Input.GetKey("c") && !song_menu_opened && !map_opened)
        {
            if (!Input.GetKey(KeyCode.LeftControl))
            {
                totalXRot = 0;
                totalYRot = 0;
            }
            if (Input.GetKey(KeyCode.LeftControl))
            {
                totalXRot = 180;
                totalYRot = 0;
            }
        }
    }


    private void FixedUpdate()
    {
        // Movement management
        if (can_move)
        {
            inputVertical = Input.GetAxis("Vertical");
            inputHorizontal = Input.GetAxis("Horizontal");
            inputUpward = Input.GetAxis("Jump");

            animator.SetFloat("fly", inputVertical);

            // Rotation controller, designed to avoid z-axis rotation that can occur from summing x and y rotations
            totalXRot += Input.GetAxis("Mouse X") * rotateSpeedX;
            totalYRot -= Input.GetAxis("Mouse Y") * rotateSpeedY;

            transform.forward = camera.transform.forward;

            if (inputVertical > 0)
            {
                camera.transform.rotation = Quaternion.Euler(totalYRot, totalXRot, 0f);
            }
            else
            {
                camera.transform.rotation = transform.rotation;
                transform.rotation = Quaternion.Euler(0f, totalXRot, 0f);
                camera.transform.rotation = Quaternion.Euler(totalYRot, totalXRot, 0f);
            }

            // Movement
            characterController.Move(camera.transform.forward * inputVertical * forwardSpeed);
            characterController.Move(camera.transform.right * inputHorizontal * forwardSpeed);
            characterController.Move(camera.transform.up * inputUpward * upwardSpeed);

            // End of movement management
        }
    }

    private void map_show()
    {
        map_opened = true;

        can_move = false;

        gameManager.view_map();
    }

    private void map_esc()
    {
        map_opened = false;

        can_move = true;

        gameManager.close_map();
    }

    private string song_menu_run()
    {
        song_menu_opened = true;

        can_move = false;

        return gameManager.start_songMenu(nearCluster);
    }

    private void song_menu_esc()
    {
        song_menu_opened = false;

        can_move = true;

        gameManager.stop_songMenu();
    }

    public void set_nearCluster(GameObject cluster, bool near_bool)
    {
        nearCluster = cluster;
        is_near = near_bool;
    }

    public void enterCluster(string cluster_id, bool is_leaf, bool starting = false, bool start_call = false)
    {
        if (start_call && !starting) // If we are calling this to start but we already started, we do not do this.
            return;

        if (!starting) {
            current_cluster_id = current_cluster_id + cluster_id;   // Update the current_cluster_id, which is kept within the player.
        }
        PlayerPrefs.SetString("current_node_id", current_cluster_id);

        if (!is_leaf)
        {
            int delay_seconds = 0;
            Invoke("load_scene", delay_seconds);
        }
        else
        {
            Debug.Log("The cluster is a leaf cluster!");
        }
        
    }

    public void setSelectedCluster(Transform selected)
    {
        selected_clust_transform = selected;
    }

    public Vector3 get_start()
    {
        Dictionary<string, string> axis = gameManager.axis;
        Dictionary<string, float> centroid = gameManager.firstCentroid;
        return new Vector3(centroid[axis["x"]] * axis_multiplier + 2, centroid[axis["y"]] * axis_multiplier,centroid[axis["z"]] * axis_multiplier);
    }


    private void OnApplicationQuit()
    {
        PlayerPrefs.DeleteAll();
    }

    private void load_scene()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex); // Reload the scene
    }

}
