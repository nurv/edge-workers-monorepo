import * as tf from "@tensorflow/tfjs";

tf.setBackend('cpu');

function toArrayBuffer(buf){
    if (Array.isArray(buf)) {
        // An Array of Buffers.
        let totalLength = 0;
        for (const buffer of buf) {
            totalLength += buffer.length;
        }

        const ab = new ArrayBuffer(totalLength);
        const view = new Uint8Array(ab);
        let pos = 0;
        for (const buffer of buf) {
            pos += buffer.copy(view, pos);
        }
        return ab;
    } else {
        // A single Buffer. Return a copy of the underlying ArrayBuffer slice.
        return buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
    }
}

export class BucketModelLoader {

    MODEL_JSON_FILENAME = 'model.json';
    WEIGHTS_BINARY_FILENAME = 'weights.bin';
    MODEL_BINARY_FILENAME = 'tensorflowjs.pb';
    MEAN_FILENAME = 'mean';
    STD_FILENAME = 'std';

    constructor(bucket, key) {
        this.path = key;
        this.bucket = bucket;
    }

    async slurp(key){
        return await this.bucket.get(key);
    }

    async save(modelArtifacts){

    }
    async load() {
        return this.loadJSONModel();
    }

    async mean(){
        return parseFloat(await this.slurp(this.path + "/" + this.MEAN_FILENAME))
    }

    async std(){
        return parseFloat(await this.slurp(this.path + "/" + this.STD_FILENAME))
    }

    async loadJSONModel(){
        const path = this.path;
        const modelJSON = JSON.parse(await this.slurp(path + "/" + this.MODEL_JSON_FILENAME));
        return tf.io.getModelArtifactsForJSON(
            modelJSON,
            (weightsManifest) => this.loadWeights(weightsManifest, path));
    }

    async loadWeights(weightsManifest, p) {
        const buffers = [];
        const weightSpecs = [];
        for (const group of weightsManifest) {
            for (const path of group.paths) {
                const buffer = await this.bucket.get(p + "/" + path);
                buffers.push(buffer);
            }
            weightSpecs.push(...group.weights);
        }
        return [weightSpecs, toArrayBuffer(buffers)];
    }
}

export class EdgeModel{
    constructor(loader, model) {
        this.loader = loader;
    }

    async load() {
        this.model = await tf.loadGraphModel(this.loader);
        this.mean = await this.loader.mean()
        this.std = await this.loader.std()
    }

    async predict(tensor){
        const tftensor = tf.tensor([tensor.map(x => (x - this.mean) / this.std)]);
        const res = await this.model.executeAsync({
            "timeseries_input_feature_input:0":tftensor
        }, ["Identity_1:0","Identity:0"]);
        const result = res[0].dataSync();
        return (result[0] * this.std) + this.mean;
    }

    static async loadModel(loader){
        const model = new EdgeModel(loader);
        await model.load();
        return model
    }
}