from selenium import webdriver
from bs4 import BeautifulSoup
import json, time

def getPlayerList(driver):
    players = {}
    driver.get("http://stats.nba.com/players/list/")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_ = 'columns / small-12 / section-view-overlay')
    for player in div.find_all('a', class_ = 'players-list__name ng-binding ng-scope'):
        tempArray = (player.text).split(', ')
        playerName = ""
        if len(tempArray) == 1:
            playerName = tempArray[0]
        else:
            playerName = tempArray[1] + ' ' + tempArray[0]
        playerLink = player['href']
        players[playerName] = {}
        players[playerName]['link'] = playerLink
    return players

def getDetailsForPlayers(driver, playerDict):
    for (player, info) in playerDict.items():
        if len(info) == 1:
            # Should look up this player
            driver.get('http://stats.nba.com%s'%(info['link']))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            time.sleep(5)
            statsPage = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/a')
            statsPage.click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            playerNames = soup.find_all('td', class_ = 'player-name first')
            trs = soup.find_all('tr', {'data-ng-repeat':"(i, row) in page track by row.$hash"})
            for tr in trs:
                tds = tr.findChildren()
                player = tds[0].text
                if len(playerDict[player]) != 1:
                    pass
                else:
                    team = tds[1].text
                    age = tds[2].text
                    height = tds[3].text
                    playerDict[str(player)]['team'] = team
                    playerDict[str(player)]['age'] = age
                    playerDict[str(player)]['height'] = height
    return playerDict

if __name__ == "__main__":
    driver = webdriver.Chrome("/Users/Danny/Desktop/chromedriver")
    playersDictionary = getPlayerList(driver)
    results = getDetailsForPlayers(driver, playersDictionary)
    with open('players.json', 'w') as file:
        json.dump(results, file)
    file.close()
    driver.quit()
