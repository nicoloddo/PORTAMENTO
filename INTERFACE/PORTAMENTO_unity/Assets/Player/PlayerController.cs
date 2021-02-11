using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    // ASSEGNAZIONI UTILI
    private Animator animator;
    private CharacterController characterController;

    // LINKS
    public GameObject camera;
    public GameManager gameManager;

    // INPUTS
    private float inputUpward; // Per muoversi verso sù
    private float inputVertical; //Tasti per muoversi in avanti
    private float inputHorizontal; //Tasti per ruotare (oltre al mouse)
    private float totalXRot; //Rotazione in X totale
    private float totalYRot; //Rotazione in Y totale

    // PARAMETRI
    private float rotateSpeedX = 4f; //Velocita' di rotazione X
    private float rotateSpeedY = 3f; //Velocita' di rotazione Y
    public float forwardSpeed = 0.5f; // Velocità di avanzamento
    public float lateralSpeed = 0.2f; // Velocità movimento laterale
    public float upwardSpeed = 0.3f; // Velocità di levitazione

    // NAVIGAZIONE
    public string current_cluster_id = "0";

    private void Awake()
    {

    }

    // Start is called before the first frame update
    void Start()
    {
        if (PlayerPrefs.HasKey("current_cluster_id"))
        {
            current_cluster_id = PlayerPrefs.GetString("current_cluster_id");
        }
        else
        {
            current_cluster_id = "0";
        }

        gameManager = FindObjectOfType<GameManager>();
        animator = GetComponent<Animator>();
        characterController = GetComponent<CharacterController>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }


    private void FixedUpdate()
    {
        inputVertical = Input.GetAxis("Vertical");
        inputHorizontal = Input.GetAxis("Horizontal"); 
        inputUpward = Input.GetAxis("Jump");

        animator.SetFloat("fly", inputVertical);

        // Controller della rotazione, è fatto così per evitare la rotazione in z, che può avvenire per somma di rotazioni in x e y
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

        // Movimento
        characterController.Move(camera.transform.forward * inputVertical * forwardSpeed);
        characterController.Move(camera.transform.right * inputHorizontal * forwardSpeed);
        characterController.Move(camera.transform.up * inputUpward * upwardSpeed);

    }

    private void OnCollisionEnter(Collision collision)
    {

    }

    private void OnCollisionExit(Collision collision)
    {
        
    }

    public void enterCluster(string cluster_id)
    {
        current_cluster_id = gameManager.runClustersInterface(current_cluster_id, cluster_id);
        PlayerPrefs.SetString("current_cluster_id", current_cluster_id);
    }


    private void OnApplicationQuit()
    {
        PlayerPrefs.DeleteAll();
    }

}
