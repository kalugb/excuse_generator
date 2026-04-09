import mongoose from "mongoose";
import dotenv from "dotenv";
import express from "express";

dotenv.config();
const PORT = process.env.PORT || 7000;
const MONGOURL = process.env.MONGO_URL;

const app = express();

const connectDB = async () => {
    try {
        await mongoose.connect(MONGOURL);
        console.log("MongoDB connected");
    } catch (err) {
        console.error(err);
        process.exit(1);
    }
};

export default connectDB;