import mongoose from "mongoose";

const excusesSchema = new mongoose.Schema({
    userID: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "User",
        required: true,
    },
    excuseInput: {
        type: String,
        required: true,
    },
    output: {
        type: String,
        required: true,
    },
    createdDate: {
        type: Date,
        default: Date.now,
        required: true
    }
});

export default mongoose.model("Excuses", excusesSchema);