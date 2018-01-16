using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour {

    public GameObject[] carGenerators;
    public static GameManager instance = null;
    public GameObject[] carPrefabs;
    public float carStartForce = 200f;
    public List<GameObject> spawnedCars = new List<GameObject>();

    public List<GameObject> intersections = new List<GameObject>();

    public int initCarsGenerated;
    public int secondsUntilNextGen;
    private int frames;

    // Use this for initialization
    void Awake()
    {
        if (instance == null)
            instance = this;
        else if (instance != this)
            Destroy(gameObject);
        frames = (int) (secondsUntilNextGen * 1 / Time.deltaTime);
        initCarsGenerated -= 1;
        Setup();
    }

    void Setup()
    {
        for (int i = 0; i < carGenerators.Length; i++)
            carGenerators[i].GetComponent<CarGeneratorScript>().Generate();
    }

    public Vector3 GetForceVectorForDirection(string direction)
    {
        Vector3 startForce = new Vector3();
        if (direction == "x+")
            startForce.x = GameManager.instance.carStartForce;
        if (direction == "z-")
            startForce.z = -GameManager.instance.carStartForce;
        if (direction == "z+")
            startForce.z = GameManager.instance.carStartForce;
        if (direction == "x-")
            startForce.x = -GameManager.instance.carStartForce;

        return startForce;
    }

    // Use this for initialization
    void Start () {

    }
    
    // Update is called once per frame
    void Update () {
        if (initCarsGenerated > 0)
        {
            if (frames == 0)
            {
                Setup();
                initCarsGenerated--;
                frames = secondsUntilNextGen * 60;
            } else
            {
                frames--;
            }
        }
    }
}
