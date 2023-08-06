import argparse
import json
from json import JSONEncoder

import numpy
import numpy as np
import torch
from flask import Flask, request
from torchvision import transforms

from definitions import SIAMESE_PATH_URL, SIAMESE_FIND_DOC_URL, MODEL_SIAMESE_PATH
from paper_neural import PaperSiamese
from paper_neural.siamese_util import match_fibers, get_model_siamese

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize(64),
    transforms.CenterCrop(60),
    # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

app = Flask(__name__)



@app.route(SIAMESE_FIND_DOC_URL, methods=["POST"])
def find_document():
    if not request.method == "POST":
        return
    json_temp = json.loads(request.json)
    target_document = np.asarray(json_temp['feature_fibers']).astype(np.float32)
    list_b = target_document.copy()


    device = torch.device('cuda') if torch.cuda.is_available else torch.device('cpu')
    target_document = torch.tensor(target_document).to(device)
    list_b = torch.tensor(list_b).to(device)

    matches = paper_yolo_siamese.matches(target_document,list_b)
    return json.dumps({"matches":matches}, cls=NumpyArrayEncoder)


@app.route(SIAMESE_PATH_URL, methods=["POST"])
def match_lists():
    if not request.method == "POST":
        return
    json_temp = request.json
    list_a = np.asarray(json_temp['a']).astype(np.float32)
    list_b = np.asarray(json_temp['b']).astype(np.float32)

    distances = np.ones(shape=(list_a.shape[0], list_b.shape[0]))

    for i in range(list_a.shape[0]):
        t_img_a = preprocess(list_a[i]).to(device).unsqueeze(0)
        for j in range(list_b.shape[0]):
            t_img_b = preprocess(list_b[j]).to(device).unsqueeze(0)
            print(i, j)
            with torch.no_grad():
                output = siamesa_model(t_img_a, t_img_b)
                #
                # out_a = siamesa_model.feature(t_img_a)
                # out_b = siamesa_model.feature(t_img_b)
                # out = siamesa_model.discriminator(out_a,out_b)

                distances[i][j] = output.cpu().numpy()[0][0]
            # print(output)
    matches = match_fibers(distances, max_distance=0.4)
    print(matches)
    # plot_pair_match(matches, list_a, list_b)
    return json.dumps({"matches":matches}, cls=NumpyArrayEncoder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5001, type=int, help="port number")
    args = parser.parse_args()
    device = torch.device('cuda') if torch.cuda.is_available else torch.device('cpu')
    paper_yolo_siamese = PaperSiamese(MODEL_SIAMESE_PATH, device)
    siamesa_model = get_model_siamese(MODEL_SIAMESE_PATH)
    siamesa_model = siamesa_model.to(device)
    app.run(host="0.0.0.0", port=args.port, debug=True)  # debug=True causes Restarting with stat