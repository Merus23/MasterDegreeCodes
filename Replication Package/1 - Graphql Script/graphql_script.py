#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import name
from github import Github, RateLimitExceededException
import csv, json, os.path, pandas as pd, requests, time
from datetime import datetime
import re
from Queries.QueryBuilder import chatgptQuery, geminiQuery, searchLLMQuery, query_composer

def run_query(query): 
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))       

class Read_contributors():

    def __init__(self, repo):
        self._repo = repo

    def requisicao_api(self):
        resposta = requests.get(
            f'https://api.github.com/repos/{self._repo}/contributors?per_page=100&anon=true', headers=headers)
        if resposta.status_code == 200:
            return resposta.json()
        else:
            return resposta.status_code

    def getContributorsCount(self):
        contributors = []
        dados_api = self.requisicao_api()
        if type(dados_api) is not int:
            return len(dados_api)
        else:
            print(dados_api)
            return None           


def getReadabilityPullRequests(): 
    
    filename = 'output/chatgpt - candidate samples.csv'

    cursor = None
    has_next_page = True    

    page_cursor = None
    has_more_files = True
    
    prs = []


    try:                    
        
        while has_next_page:

            result = run_query(query_composer(cursor, page_cursor))
            end_cursor = result["data"]["search"]["pageInfo"]["endCursor"]
            has_next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]

            issueCount = result["data"]["search"]["issueCount"]
        
            print(f"Occurrences: {issueCount}")
            print(f"Processando página com cursor: {cursor}")

            for pr in result["data"]["search"]["edges"]:   
                pr_url = pr["node"]["url"]
                pr_title = pr["node"]["title"]
                pr_created_at = pr["node"]["createdAt"]
                pr_merged_at = pr["node"]["mergedAt"]
                pr_state = pr["node"]["state"]                                                                               
                stars = pr["node"]["repository"]["stargazerCount"]
                fork = pr["node"]["repository"]["isFork"]
                language = ""
                if pr["node"]["repository"]["primaryLanguage"] != None:
                    language = pr["node"]["repository"]["primaryLanguage"]["name"]

                # Pagination in files
                has_more_files = pr["node"]["files"]["pageInfo"]["hasNextPage"]
                page_cursor = None
                has_test_file = False

                while has_more_files:
                    try:
                        if page_cursor:
                            pr_files_result = run_query(query_composer(cursor, page_cursor))
                            # Verificar se há edges antes de acessar
                            if pr_files_result["data"]["search"]["edges"]:
                                pr_files = pr_files_result["data"]["search"]["edges"][0]["node"]["files"]
                            else:
                                print(f"Não há mais arquivos para processar no PR {pr_url}")
                                break
                        else:
                            pr_files = pr["node"]["files"]
                        
                        if not pr_files["edges"]:
                            print(f"Não há arquivos nesta página para o PR {pr_url}")
                            break
                            
                        page_cursor = pr_files["pageInfo"]["endCursor"]
                        has_more_files = pr_files["pageInfo"]["hasNextPage"]
                        
                        print(f"Processando arquivos do PR {pr_url} com cursor: {page_cursor}")
                        
                        for file_edge in pr_files["edges"]:
                            file_path = file_edge["node"]["path"]
                            if "test" in file_path.lower():
                                has_test_file = True
                                print(f"Arquivo de teste encontrado: {file_path}")
                            else:
                                print(f"Arquivo regular encontrado: {file_path}")
                                
                    except Exception as e:
                        print(f"Erro ao processar arquivos do PR {pr_url}: {str(e)}")
                        break


                repo_name = extract_repository_name(pr_url)
                read_contributors = Read_contributors(repo_name)  
                contributors_count = read_contributors.getContributorsCount()

                if stars >= min_stars and fork == False and has_test_file == True:                                                
                    if contributors_count > min_contributors:
                        prs.append((pr_url, pr_title, pr_created_at, pr_merged_at, pr_state, stars, fork, contributors_count, language))                            
                else:
                    print(f"Repo {repo_name} rejected: stars - {stars} contributors - {contributors_count} - fork {fork}")

            cursor = end_cursor

        prs.sort(key=lambda x: x[0], reverse=True)

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['PR URL', 'PR Title', 'PR createdAt', 'PR mergedAt', 'PR state', 'stars', 'fork', 'collaborators','language'])
            writer.writerows(prs)               

    except Exception as e:
        error_detail = result.get('errors', 'No additional error details available.')
        print(f"{e}. Additional details: {error_detail}")


def extract_repository_name(url):
    match = re.search(r"github\.com/([^/]+/[^/]+)", url)
    if match:
        nome_repositorio = match.group(1)
        return nome_repositorio
    else:
        return "Repositório não encontrado."
        

# GRAPHQL API v4
access_token = os.getenv('GITHUB_API_KEY')
headers = {'Authorization': 'Bearer '+ access_token}

min_stars = 1
min_contributors = 1

getReadabilityPullRequests()




