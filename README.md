
# Real-Time Twitter Sentiment Analysis Pipeline with Spark & Kafka

This project is a complete, end-to-end data engineering pipeline that captures  tweets from the Twitter API (or data set), processes them in real-time using Apache Spark, and performs sentiment analysis. The processed data is structured to be consumed by a front-end dashboard for visualization.

## ⚙️ Pipeline Architecture

The pipeline follows a classic producer-consumer architecture, ensuring scalability and fault tolerance.

**Data Flow:**
`Twitter API` → `producer.py` → `Apache Kafka` → `consumer.py (Spark Streaming)` → `Analyzed Output (Console/Dashboard)`

-----

## 📁 Repository Contents

This repository contains the core scripts for the data pipeline:

  * **`producer.py`**: The **Data Collector** 📥. This script connects to the Twitter API, fetches live tweets based on a specified keyword, and pushes them into a Kafka topic.
  * **`consumer.py`**: The **Data Processor** 🧠. This script uses Spark Streaming to connect to the Kafka topic, read the tweets in real-time, perform sentiment analysis on each tweet using `TextBlob`, and output the results.
  * **`config.py`**: **Configuration & Security** 🔑. Stores the necessary Twitter API keys and tokens. This file is included in `.gitignore` to prevent accidental exposure of credentials.
  * **`requirements.txt`**: The **Dependency List** 📋. Contains all the necessary Python libraries to run the project.

-----

## 🚀 Sample Application Dashboard

The data processed by this pipeline is designed to power a real-time analytics dashboard. The screenshots below are from a sample front-end application built with **Streamlit** to demonstrate the potential visualizations and insights.

  * **Interactive Filters & Charts:** Users can filter tweets by sentiment or username, with charts updating instantly.

  * **Detailed Tweet View:** The raw, analyzed tweets can be displayed in a clean, tabular format.

  * **Trending Topics:** A word cloud can be generated to visualize the most frequently discussed words in the tweet stream.
Screenshot of the current version are: 

<img width="1866" height="441" alt="image" src="https://github.com/user-attachments/assets/e6203f46-4a96-4592-8e57-b7a94e7069d4" />
<img width="1702" height="651" alt="image" src="https://github.com/user-attachments/assets/24a85920-8e15-479c-a7a3-fa31a11e5381" />
<img width="1740" height="828" alt="image" src="https://github.com/user-attachments/assets/3d7bb25b-8c3a-4732-84ff-ecc398909b2b" />
<img width="1795" height="729" alt="image" src="https://github.com/user-attachments/assets/4158a72c-eed2-4242-9b0d-fc528770509c" />





-----

## 🛠️ Technologies Used

  * **Backend & Processing:** Python, Apache Spark, Apache Kafka
  * **Data Source:** Tweepy (Twitter API v2)
  * **NLP:** TextBlob
  * **Sample Frontend:** Streamlit, Pandas, Plotly

-----

## ⚙️ Setup and Installation

To run this pipeline locally, you will need to have Apache Kafka and Apache Spark installed and running on your system.

1.  **Prerequisites:**

      * Start your Zookeeper and Kafka servers.
      * Ensure your Spark instance is running.

2.  **Clone the repository:**

    ```bash
    git clone https://github.com/ChiragSaxena5437/spark_stream.git
    cd spark_stream
    ```

3.  **Configure API Keys:**

      * Rename `config.py.template` to `config.py`.
      * Add your own Twitter API keys and access tokens to the `config.py` file.

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Pipeline:**

      * Open a terminal window and start the Spark consumer to listen for data:
        ```bash
        python consumer.py
        ```
      * Open a **second** terminal window and start the producer to fetch tweets:
        ```bash
        python producer.py
        ```

You will now see the analyzed tweets being printed in the consumer's terminal window.
