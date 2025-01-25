package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"time"

	"github.com/go-redis/redis/v8"
	_ "github.com/lib/pq"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var ctx = context.Background()

// PostgreSQL
func writeToPostgreSQL() {
	connStr := "host=postgres_container dbname=mydb user=user password=password sslmode=disable"
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatalf("PostgreSQL bağlantısı başarısız: %v", err)
	}
	defer db.Close()

	_, err = db.Exec("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, data TEXT);")
	if err != nil {
		log.Fatalf("PostgreSQL tablo oluşturulamadı: %v", err)
	}

	_, err = db.Exec("INSERT INTO test (data) VALUES ($1)", "Hello Abdullah Karakoç!")
	if err != nil {
		log.Fatalf("PostgreSQL veri eklenemedi: %v", err)
	}

	var data string
	err = db.QueryRow("SELECT data FROM test ORDER BY id DESC LIMIT 1").Scan(&data)
	if err != nil {
		log.Fatalf("PostgreSQL veri sorgulanamadı: %v", err)
	}

	fmt.Println("PostgreSQL:", data)
}

// MongoDB
func writeToMongo() {
	clientOptions := options.Client().ApplyURI("mongodb://mongo_container:27017")
	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		log.Fatalf("MongoDB bağlantısı başarısız: %v", err)
	}
	defer client.Disconnect(ctx)

	collection := client.Database("test_db").Collection("test_collection")

	_, err = collection.InsertOne(ctx, bson.M{"message": "Hello, Abdullah Karakoç!"})
	if err != nil {
		log.Fatalf("MongoDB veri eklenemedi: %v", err)
	}

	var result bson.M
	err = collection.FindOne(ctx, bson.M{"message": "Hello, Abdullah Karakoç!"}).Decode(&result)
	if err != nil {
		log.Fatalf("MongoDB veri sorgulanamadı: %v", err)
	}

	fmt.Println("MongoDB:", result["message"])
}

// Redis
func writeToRedis() {
	rdb := redis.NewClient(&redis.Options{
		Addr: "redis_container:6379",
	})
	defer rdb.Close()

	err := rdb.Set(ctx, "message", "Hello, Abdullah Karakoç!", 0).Err()
	if err != nil {
		log.Fatalf("Redis veri eklenemedi: %v", err)
	}

	val, err := rdb.Get(ctx, "message").Result()
	if err != nil {
		log.Fatalf("Redis veri sorgulanamadı: %v", err)
	}

	fmt.Println("Redis:", val)
}

func main() {
	fmt.Println("WAITING")
	time.Sleep(30 * time.Second)

	fmt.Println("WRITING DATA")
	writeToPostgreSQL()
	writeToMongo()
	writeToRedis()
}

