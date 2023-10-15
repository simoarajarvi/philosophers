import os
from flask import Flask, render_template, url_for, request, jsonify, session
from datetime import datetime
import doc_handler
import configparser
import logging
import logging.config

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/query', methods=['POST', 'GET'])
def handle_query():
  if request.method == "POST":
    query_txt = request.get_json()[0]['query']
    num_experts = int(request.get_json()[0]['numExperts'])
    logger.info('Query text: '+query_txt)
    logger.info('Num experts requested: '+str(num_experts))
    embedding_list = doc_handler.get_embeddings_as_list()
    exp_embeddings = []
    for inx,embedding in enumerate(embedding_list):
      exp_embeddings += [embedding[1]]
   
    # Get embedding for the query
    qry_embedding = doc_handler.get_embedding_for_question(doc_handler.doc_text_to_clean(query_txt))
    
    # Find the most similar documents
    dist_metric = config.get('embeddings','dist_metric')
    best_experts,distances = doc_handler.find_best_experts(qry_embedding,exp_embeddings,dist_metric)

    mean_distance = sum(distances)/len(distances)
    std_distance = (sum([(x-mean_distance)**2 for x in distances])/len(distances))**0.5
    logger.debug('Mean distance - '+mean_distance)
    logger.debug('Std distance - '+std_distance)

    # Sort out the best experts
    candidates = []
    star_scores = []
    i = 0
    for inx in best_experts: 
      i +=1
      exp = embedding_list[inx][0]
      distance = distances[inx]
      print(exp[0],' ->',round(distance,4))
      if i <= num_experts:
        candidates.append(exp[0])
        std_dist_score = abs(round((distance-mean_distance)/std_distance))+2
   
        if std_dist_score > 5:
          std_dist_score = 5
        else:
          std_dist_score = std_dist_score
        star_scores.append(std_dist_score)

    # Get the most similar documents    
    temp = config.get('generator','temperature')  
    mdl = config.get('generator','engine')  
    results = doc_handler.generate(candidates,star_scores,query_txt,mdl,temp)
    results = results[0:num_experts] # Drop the last one, which is the query itself
    
  return jsonify(results)


# Startup functions
def init_cache():
  doc_handler.build_embed_cache()
  
def setup_config():
  config = configparser.ConfigParser()
  config.read(os.path.join(basedir, 'config.ini'))
  return config

if __name__ == "__main__":
  config = setup_config()
  logging.config.fileConfig('logging.conf')
  logger = logging.getLogger(__name__)
  logger.info('Server booting up...')
  logger.info('App version: '+ config.get('app_info', 'version'))
  exp_embeddings = init_cache()
  app.run(debug=True)